from fastapi import APIRouter
from typing import List, Optional, Dict, Any
from app.config import settings
import io
import tarfile
import docker


router = APIRouter(prefix="/api/sandbox", tags=["sandbox"])


DOCKERFILES: Dict[str, str] = {
    "python": """
# Bug Ghost AI - Python Sandbox
FROM python:3.11-slim
RUN useradd -m -u 1000 -s /bin/bash sandbox
RUN mkdir /workspace && chown sandbox:sandbox /workspace
WORKDIR /workspace
RUN pip install --no-cache-dir pytest requests
USER sandbox
CMD ["python", "--version"]
""".strip(),
    "node": """
# Bug Ghost AI - Node.js Sandbox
FROM node:20-alpine
RUN deluser node 2>/dev/null || true && \
    adduser -D -u 1000 sandbox
RUN mkdir /workspace && chown sandbox:sandbox /workspace
WORKDIR /workspace
RUN npm install -g typescript ts-node jest
USER sandbox
CMD ["node", "--version"]
""".strip(),
    "java": """
# Bug Ghost AI - Java Sandbox
FROM eclipse-temurin:17-jdk-alpine
RUN deluser $(getent passwd 1000 | cut -d: -f1) 2>/dev/null || true && \
    adduser -D -u 1000 sandbox
RUN mkdir /workspace && chown sandbox:sandbox /workspace
WORKDIR /workspace
USER sandbox
CMD ["java", "--version"]
""".strip(),
}


IMAGES = {
    "python": "bug-ghost-sandbox-python:latest",
    "javascript": "bug-ghost-sandbox-node:latest",
    "node": "bug-ghost-sandbox-node:latest",
    "typescript": "bug-ghost-sandbox-node:latest",
    "java": "bug-ghost-sandbox-java:latest",
}


def _docker_client():
    # Connect to DinD or local Docker depending on settings
    if settings.DOCKER_HOST:
        return docker.DockerClient(base_url=settings.DOCKER_HOST)
    return docker.from_env()


def _build_image_from_dockerfile(client: docker.DockerClient, dockerfile_text: str, tag: str) -> List[str]:
    # Create an in-memory tar context with a single Dockerfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tar:
        data = dockerfile_text.encode("utf-8")
        ti = tarfile.TarInfo(name="Dockerfile")
        ti.size = len(data)
        tar.addfile(ti, io.BytesIO(data))
    buf.seek(0)

    logs: List[str] = []
    # Use low-level API for fileobj builds
    for chunk in client.api.build(fileobj=buf, customcontext=True, tag=tag, decode=True, dockerfile="Dockerfile"):
        if "stream" in chunk:
            line = chunk["stream"].strip()
            if line:
                logs.append(line)
        if "error" in chunk:
            logs.append(f"ERROR: {chunk['error']}")
            break
    return logs


@router.get("/images")
def list_sandbox_images() -> Dict[str, Any]:
    client = _docker_client()
    present: Dict[str, bool] = {}
    for lang, tag in IMAGES.items():
        try:
            imgs = client.images.list(name=tag)
            present[tag] = any(tag in (img.tags or []) for img in imgs)
        except Exception:
            present[tag] = False
    return {"images": present}


@router.post("/images/build")
def build_sandbox_images(languages: Optional[List[str]] = None) -> Dict[str, Any]:
    # Default to building canonical set
    langs = languages or ["python", "javascript", "java"]
    # De-duplicate/normalize
    norm = []
    for l in langs:
        l = l.lower()
        if l == "javascript" or l == "typescript":
            l = "node"  # Build node image for JS/TS
        if l not in norm:
            norm.append(l)

    client = _docker_client()
    results: Dict[str, Any] = {}
    for l in norm:
        if l not in DOCKERFILES:
            results[l] = {"built": False, "error": "unsupported language"}
            continue
        tag = IMAGES.get(l, IMAGES["python"]) if l != "node" else IMAGES["node"]
        logs = _build_image_from_dockerfile(client, DOCKERFILES[l], tag)
        results[l] = {"built": True, "image": tag, "logs": logs[-20:]}  # return tail of logs

    return {"results": results}
