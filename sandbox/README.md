# Bug Ghost AI Sandbox Images 🔒

Secure, minimal Docker images for executing user-submitted code.

## Overview

Each sandbox image is designed with security and isolation in mind:

- **Non-root user**: All code runs as `uid=1000` (user `sandbox`)
- **Minimal base**: Alpine or slim variants to reduce attack surface
- **Working directory**: `/workspace` for code execution
- **No network**: Network is disabled at container creation
- **Resource limits**: 256MB RAM, ~50% CPU enforced by Docker

## Available Images

### Python (`sandbox-python`)

**Base**: `python:3.11-slim`  
**Installed**: `pytest`, `requests`  
**Usage**: Python scripts (`.py`)

```bash
docker build -t bug-ghost-sandbox-python:latest ./python
```

### Node.js (`sandbox-node`)

**Base**: `node:20-alpine`  
**Installed**: `typescript`, `ts-node`, `jest`  
**Usage**: JavaScript (`.js`), TypeScript (`.ts`)

```bash
docker build -t bug-ghost-sandbox-node:latest ./node
```

### Java (`sandbox-java`)

**Base**: `eclipse-temurin:17-jdk-alpine`  
**Installed**: JDK 17  
**Usage**: Java source files (`.java`)

```bash
docker build -t bug-ghost-sandbox-java:latest ./java
```

## Adding a New Language

1. **Create directory**: `sandbox/<language>/`
2. **Write Dockerfile**:
   ```dockerfile
   FROM <base-image>
   RUN adduser -D -u 1000 sandbox
   RUN mkdir /workspace && chown sandbox:sandbox /workspace
   WORKDIR /workspace
   USER sandbox
   CMD ["<runtime>", "--version"]
   ```
3. **Add to docker-compose.yml**:
   ```yaml
   sandbox-<language>:
     build:
       context: ./sandbox/<language>
     image: bug-ghost-sandbox-<language>:latest
     profiles: ["build-only"]
   ```
4. **Update SandboxRunner**: Edit `backend/app/services/sandbox_runner.py`
5. **Build**: `docker-compose build sandbox-<language>`

## Security Considerations

### What's Protected

✅ No network access (enforced by Docker)  
✅ Non-root execution (uid 1000)  
✅ Resource limits (memory, CPU)  
✅ Time limits (enforced by backend)  
✅ No host filesystem access  

### What's NOT Protected

⚠️ Fork bombs (limited by cgroup but can impact DinD)  
⚠️ Disk fill (containers share DinD storage)  
⚠️ CPU-intensive loops (mitigated by CPU quota)  

### Production Recommendations

For production deployments:

- Use gVisor or Kata Containers for additional isolation
- Implement per-user rate limiting
- Monitor DinD resource usage
- Consider dedicated sandbox nodes
- Enable Docker Content Trust for image verification

## Image Maintenance

### Updating Base Images

```bash
# Pull latest base images
docker pull python:3.11-slim
docker pull node:20-alpine
docker pull eclipse-temurin:17-jdk-alpine

# Rebuild sandboxes
docker-compose build sandbox-python sandbox-node sandbox-java
```

### Adding Dependencies

Edit the respective Dockerfile and rebuild:

```dockerfile
# Example: Add numpy to Python sandbox
RUN pip install --no-cache-dir pytest requests numpy pandas
```

Then rebuild:
```bash
docker-compose build sandbox-python
```

## Testing Locally

```bash
# Test Python sandbox
docker run --rm -u 1000:1000 --network none \
  bug-ghost-sandbox-python:latest \
  python -c "print('Hello from sandbox!')"

# Test Node sandbox
docker run --rm -u 1000:1000 --network none \
  bug-ghost-sandbox-node:latest \
  node -e "console.log('Hello from sandbox!')"

# Test Java sandbox
echo "public class Main { public static void main(String[] args) { System.out.println(\"Hello!\"); } }" > Main.java
docker run --rm -u 1000:1000 --network none -v $(pwd):/workspace \
  bug-ghost-sandbox-java:latest \
  bash -c "javac Main.java && java Main"
```

## Troubleshooting

### "Image not found" errors

Build the images first:
```bash
docker-compose build sandbox-python sandbox-node sandbox-java
```

### "Permission denied" errors

Ensure files are created with correct ownership inside container (handled automatically by SandboxRunner).

### "Network is unreachable" errors

This is expected! Network is disabled for security.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on adding new language support.

---

**Security Notice**: These images are designed for isolated, short-lived code execution. Do not use for long-running processes or as general-purpose containers.
