# Contributing to Bug Ghost AI 👻🐛

Thank you for your interest in contributing to Bug Ghost AI! This guide will help you get started.

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (required for sandbox execution)
- **Node.js** 18+ and npm
- **Python** 3.11+
- **OpenAI or Anthropic API key**

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Phantasm0009/bug-ghost-ai.git
   cd bug-ghost-ai
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your LLM_API_KEY
   
   # Frontend
   cp frontend/.env.example frontend/.env.local
   ```

3. **Build sandbox images (first time only)**
   ```bash
   docker-compose build sandbox-python sandbox-node sandbox-java
   ```

4. **Start all services**
   ```bash
   docker-compose up -d
   ```

5. **Verify everything is running**
   ```bash
   # Backend health
   curl http://localhost:8000/health
   
   # Frontend
   open http://localhost:3000
   
   # API docs
   open http://localhost:8000/docs
   ```

---

## 🧪 Sandbox Execution System

Bug Ghost AI uses **Docker-in-Docker (DinD)** to safely execute user-submitted code.

### How It Works

1. **DinD Service**: A privileged Docker daemon runs inside Compose (`dind` service)
2. **Backend**: Connects to DinD via `DOCKER_HOST=tcp://dind:2375`
3. **Sandbox Images**: Pre-built minimal images with non-root users
4. **Execution**: Code is injected, run with strict limits, then container is destroyed

### Security Features

- ✅ **Non-root user** (`uid=1000`) inside containers
- ✅ **Network disabled** by default
- ✅ **Resource limits**: 256MB RAM, ~50% CPU
- ✅ **Time limits**: 10-60 second timeout
- ✅ **No host mounts**: Code passed via in-memory tar

### Testing Sandbox Locally

```bash
# Test Python execution
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello from sandbox!\")"
  }'

# Test JavaScript
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "console.log(\"Hello from Node!\");"
  }'
```

---

## 🆕 Adding a New Language

Want to add support for Ruby, Go, Rust, or another language? Here's how:

### 1. Create Sandbox Dockerfile

Create `sandbox/<language>/Dockerfile`:

```dockerfile
# Example: sandbox/ruby/Dockerfile
FROM ruby:3.2-alpine
RUN adduser -D -u 1000 sandbox
RUN mkdir /workspace && chown sandbox:sandbox /workspace
WORKDIR /workspace
USER sandbox
CMD ["ruby", "--version"]
```

### 2. Add to docker-compose.yml

```yaml
  sandbox-ruby:
    build:
      context: ./sandbox/ruby
    image: bug-ghost-sandbox-ruby:latest
    profiles: ["build-only"]
```

### 3. Update SandboxRunner

Edit `backend/app/services/sandbox_runner.py` to add language mapping and command.

### 4. Build and Test

```bash
docker-compose build sandbox-ruby
curl -X POST http://localhost:8000/api/runs \
  -d '{"language": "ruby", "code": "puts \"Hello!\""}'
```

---

## Commit Convention

We use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all checks pass
4. Request review from maintainers
5. Address review feedback
6. Once approved, we'll merge!

## Questions?

Open an issue or join our discussions!

Thank you for contributing! 🙏
