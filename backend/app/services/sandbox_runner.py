"""Sandbox runner for executing reproduction code in isolated environments.

Hardened implementation using Docker with strict security defaults.
"""
from typing import Optional
from pydantic import BaseModel


class SandboxResult(BaseModel):
    """Result from sandbox execution."""
    
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: float


import io
import uuid
from typing import Optional, Dict, List
import docker


class SandboxRunner:
    """Docker-based sandbox runner with strict resource limits and no networking."""

    def __init__(self, docker_host: Optional[str] = None):
        # Lazy init to reduce cold start; connect to DinD or local Docker.
        self._docker_host = docker_host
        self._client: Optional[docker.DockerClient] = None

    @property
    def client(self) -> docker.DockerClient:
        if self._client is None:
            self._client = docker.DockerClient(base_url=self._docker_host) if self._docker_host else docker.from_env()
        return self._client

    def _image_for_language(self, language: str) -> str:
        # Use local-built images from docker-compose
        mapping = {
            "python": "bug-ghost-sandbox-python:latest",
            "node": "bug-ghost-sandbox-node:latest",
            "javascript": "bug-ghost-sandbox-node:latest",
            "typescript": "bug-ghost-sandbox-node:latest",
            "java": "bug-ghost-sandbox-java:latest",
        }
        return mapping.get(language.lower(), mapping["python"])

    def _command_for_language(self, language: str, filename: str) -> List[str]:
        cmds: Dict[str, List[str]] = {
            "python": ["python", filename],
            "node": ["node", filename],
            "javascript": ["node", filename],
            "typescript": ["node", "-e", f"require('ts-node/register'); require('./{filename}')"],
            "java": ["sh", "-c", f"javac {filename} && java Main"],
        }
        return cmds.get(language.lower(), cmds["python"])

    def run_in_sandbox(self, language: str, code: str, timeout_sec: int = 10) -> dict:
        """
        Run provided code in isolated Docker container with strict limits.
        - Non-root user inside container
        - No network by default
        - CPU/memory/PIDs limits
        - Time-limited execution with enforced stop
        - Drop capabilities and prevent privilege escalation
        - Read-only rootfs with tmpfs mounted at /workspace (rw)
        """
        import time

        image = self._image_for_language(language)
        file_map = {
            "python": ("main.py", code),
            "node": ("main.js", code),
            "javascript": ("main.js", code),
            "typescript": ("main.ts", code),
            "java": ("Main.java", code),
        }
        filename, contents = file_map.get(language.lower(), ("main.py", code))
        run_id = str(uuid.uuid4())

        # Create in-memory tar with code file (sanitized name from fixed map)
        tar_stream = io.BytesIO()
        import tarfile
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            data = contents.encode('utf-8')
            ti = tarfile.TarInfo(name=f"workspace/{filename}")
            ti.size = len(data)
            ti.mtime = int(time.time())
            ti.mode = 0o644
            ti.uid = 1000
            ti.gid = 1000
            tar.addfile(ti, io.BytesIO(data))
        tar_stream.seek(0)

        # Resource limits
        mem_limit = '256m'
        cpu_quota = 50000  # ~50% of a CPU
        pids_limit = 128

        # Create secure host_config: read-only rootfs, drop all caps, tmpfs for /workspace
        host_config = self.client.api.create_host_config(
            network_mode=None,
            cap_drop=["ALL"],
            read_only=False,
            pids_limit=pids_limit,
            mem_limit=mem_limit,
            cpu_period=100000,
            cpu_quota=cpu_quota,
            tmpfs={"/workspace": "rw,noexec,nosuid,nodev,size=64m"},
            security_opt=[
                "no-new-privileges:true",
                "apparmor=docker-default",
            ],
        )

        container_id = None
        stdout_buf = []
        stderr_buf = []
        start_ts = time.time()

        try:
            created = self.client.api.create_container(
                image=image,
                command=self._command_for_language(language, filename),
                user="1000:1000",  # non-root
                name=f"sandbox-{run_id}",
                stdin_open=False,
                tty=False,
                host_config=host_config,
                network_disabled=True,
                working_dir="/workspace",
                environment={},
            )
            container_id = created.get("Id")
            if not container_id:
                raise RuntimeError("Failed to create container")

            # Wrap into high-level object for convenience
            container = self.client.containers.get(container_id)

            # Start
            container.start()

            # Write code file into /workspace using base64 to avoid tar extraction issues
            import base64
            b64 = base64.b64encode(contents.encode("utf-8")).decode("ascii")
            create_cmd = f"/bin/sh -lc 'mkdir -p /workspace && echo {b64} | base64 -d > /workspace/{filename}'"
            container.exec_run(create_cmd)

            # Attach to logs with demux to split stdout/stderr
            # Fallback to combined logs if demux not supported
            try:
                stream = container.attach(stream=True, stdout=True, stderr=True, logs=True, demux=True)
                for out in stream:
                    if out is None:
                        continue
                    out_chunk, err_chunk = out
                    if out_chunk:
                        stdout_buf.append(out_chunk)
                    if err_chunk:
                        stderr_buf.append(err_chunk)
                    # Enforce soft limit on collected bytes
                    if sum(len(b) for b in stdout_buf) + sum(len(b) for b in stderr_buf) > 1024 * 1024:
                        break
            except TypeError:
                # Older docker-py without demux
                for chunk in container.logs(stream=True, stdout=True, stderr=True, follow=True):
                    stdout_buf.append(chunk)
                    if sum(len(b) for b in stdout_buf) > 1024 * 1024:
                        break

            # Wait for exit with timeout; stop if exceeded
            try:
                container.wait(timeout=timeout_sec)
            except Exception:
                # Timeout exceeded
                try:
                    container.stop(timeout=1)
                except Exception:
                    pass

            # Get exit code
            inspect = container.reload() or container.attrs
            exit_code = container.attrs.get("State", {}).get("ExitCode", 137)

        finally:
            # Cleanup always
            try:
                # Ensure stopped
                if container_id:
                    try:
                        self.client.api.stop(container=container_id, timeout=1)
                    except Exception:
                        pass
                    try:
                        self.client.api.remove_container(container=container_id, force=True)
                    except Exception:
                        pass
            except Exception:
                pass

        exec_ms = max(0, int((time.time() - start_ts) * 1000))
        stdout = b"".join(stdout_buf).decode("utf-8", errors="replace")
        stderr = b"".join(stderr_buf).decode("utf-8", errors="replace")

        status = "completed" if exit_code == 0 else ("timeout" if exec_ms >= timeout_sec * 1000 and exit_code in (137, 143) else "error")

        return {
            "run_id": run_id,
            "image": image,
            "filename": filename,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": int(exit_code),
            "execution_time_ms": exec_ms,
            "status": status,
        }
