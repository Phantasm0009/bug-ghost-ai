"""Tests for SandboxRunner security and result shape.

Skips if Docker is unavailable in the environment.
"""
import os
import pytest

from app.services.sandbox_runner import SandboxRunner


def docker_available() -> bool:
    try:
        import docker  # noqa: F401
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not docker_available(), reason="Docker not available for tests")


def test_sandbox_runner_python_basic():
    runner = SandboxRunner(docker_host=os.environ.get("DOCKER_HOST"))
    code = "print('hello'); import sys; sys.stderr.write('oops\n')"
    result = runner.run_in_sandbox("python", code, timeout_sec=5)

    assert isinstance(result, dict)
    assert result.get("run_id")
    assert result.get("image")
    assert "stdout" in result and "stderr" in result
    assert "exit_code" in result and isinstance(result["exit_code"], int)
    assert "execution_time_ms" in result
    assert result.get("status") in {"completed", "error", "timeout"}
