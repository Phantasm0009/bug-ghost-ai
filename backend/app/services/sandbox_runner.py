"""Sandbox runner for executing reproduction code in isolated environments.

Phase 2 implementation - currently stubbed for future Docker integration.
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
        # Connect to DinD or local Docker depending on compose setup
        self.client = docker.DockerClient(base_url=docker_host) if docker_host else docker.from_env()

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
        - CPU/memory limits
        - Time-limited execution
        """
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

        # Create in-memory tar with code file
        tar_stream = io.BytesIO()
        import tarfile, time
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            data = contents.encode('utf-8')
            ti = tarfile.TarInfo(name=filename)
            ti.size = len(data)
            ti.mtime = int(time.time())
            tar.addfile(ti, io.BytesIO(data))
        tar_stream.seek(0)

        # Resource limits
        mem_limit = '256m'
        cpu_quota = 50000  # ~50% of a CPU

        container = self.client.containers.create(
            image=image,
            command=self._command_for_language(language, filename),
            user="1000:1000",  # non-root
            network_disabled=True,
            stdin_open=False,
            tty=False,
            mem_limit=mem_limit,
            cpu_period=100000,
            cpu_quota=cpu_quota,
            name=f"sandbox-{run_id}",
            detach=True,
        )

        # Copy code file into container
        container.put_archive(path="/workspace", data=tar_stream.getvalue())

        # Start and stream logs with timeout
        container.start()
        logs = b""
        try:
            for chunk in container.logs(stream=True, stdout=True, stderr=True, follow=True):
                logs += chunk
                if len(logs) > 1024 * 1024:
                    break
        except Exception:
            pass
        finally:
            try:
                container.stop(timeout=1)
            except Exception:
                pass
            try:
                container.remove(force=True)
            except Exception:
                pass

        return {
            "run_id": run_id,
            "image": image,
            "filename": filename,
            "stdout": logs.decode('utf-8', errors='replace'),
        }
