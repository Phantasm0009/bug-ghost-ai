# Sandbox Quick Start Guide 🚀

Test the Bug Ghost AI sandbox execution system in 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Bug Ghost AI repository cloned
- `.env` configured with LLM API key

## Setup (One Time)

```bash
# Navigate to project root
cd bug-ghost-ai

# Build sandbox images
./setup-sandbox.sh  # Linux/Mac
# OR
setup-sandbox.bat   # Windows

# Start all services
docker-compose up -d

# Wait for services to be healthy (30-60 seconds)
docker-compose ps
```

## Test Python Sandbox

```bash
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Hello from Python sandbox!\")\nfor i in range(5):\n    print(f\"Count: {i}\")\nimport sys\nprint(f\"Python version: {sys.version}\")"
  }'
```

Expected output:
```json
{
  "run_id": "...",
  "language": "python",
  "status": "completed",
  "stdout": "Hello from Python sandbox!\nCount: 0\nCount: 1\nCount: 2\nCount: 3\nCount: 4\nPython version: 3.11...",
  "image": "bug-ghost-sandbox-python:latest",
  "created_at": "2025-12-01T..."
}
```

## Test JavaScript Sandbox

```bash
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "code": "console.log(\"Hello from Node!\");\nfor(let i=0; i<5; i++) {\n  console.log(`Count: ${i}`);\n}\nconsole.log(`Node version: ${process.version}`);"
  }'
```

## Test Java Sandbox

```bash
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "java",
    "code": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello from Java!\");\n        for(int i=0; i<5; i++) {\n            System.out.println(\"Count: \" + i);\n        }\n    }\n}"
  }'
```

## Test Error Handling

```bash
# Python with error
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "print(\"Starting...\")\nraise ValueError(\"This is a test error!\")\nprint(\"This won't print\")"
  }'
```

## Test Timeout

```bash
# Infinite loop (should timeout)
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import time\nwhile True:\n    print(\"Looping...\")\n    time.sleep(1)",
    "timeout_sec": 5
  }'
```

## WebSocket Log Streaming

Create a file `test-ws.html`:

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Sandbox Log Stream Test</h1>
  <div id="logs"></div>
  <script>
    const runId = 'YOUR_RUN_ID_HERE'; // Replace with actual run_id from API
    const ws = new WebSocket(`ws://localhost:8000/api/runs/ws/${runId}/logs`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const logsDiv = document.getElementById('logs');
      logsDiv.innerHTML += `<div>[${data.type}] ${data.data || data.status}</div>`;
    };
    
    ws.onerror = (error) => console.error('WebSocket error:', error);
    ws.onclose = () => console.log('Connection closed');
  </script>
</body>
</html>
```

## Verify Security

```bash
# Test 1: Network should be disabled
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import socket\ntry:\n    socket.create_connection((\"google.com\", 80), timeout=2)\n    print(\"FAIL: Network is available!\")\nexcept Exception as e:\n    print(f\"SUCCESS: Network blocked - {type(e).__name__}\")"
  }'

# Test 2: File system is isolated
curl -X POST http://localhost:8000/api/runs \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "code": "import os\nprint(\"User:\", os.getenv(\"USER\", \"unknown\"))\nprint(\"UID:\", os.getuid())\nprint(\"CWD:\", os.getcwd())\nprint(\"Files:\", os.listdir(\".\"))"
  }'
```

Expected:
- Network test should show "Network blocked"
- File system should show user `sandbox`, UID `1000`, CWD `/workspace`

## Monitor DinD

```bash
# Check DinD status
docker exec bug-ghost-dind docker info

# List containers created by sandbox (should be auto-cleaned)
docker exec bug-ghost-dind docker ps -a

# Check DinD logs
docker-compose logs dind
```

## Troubleshooting

### "Connection refused"

Backend not ready. Check:
```bash
docker-compose logs backend
curl http://localhost:8000/health
```

### "Image not found"

Build sandbox images:
```bash
docker-compose build sandbox-python sandbox-node sandbox-java
```

### "DinD not healthy"

Wait longer or restart:
```bash
docker-compose restart dind
docker-compose logs -f dind
```

## Clean Up

```bash
# Stop all services
docker-compose down

# Remove volumes (including DinD storage)
docker-compose down -v

# Remove sandbox images
docker rmi bug-ghost-sandbox-python bug-ghost-sandbox-node bug-ghost-sandbox-java
```

## Next Steps

- Integrate sandbox into frontend UI
- Add more languages (Ruby, Go, Rust)
- Implement persistent run history in database
- Add rate limiting per user
- Deploy to Railway or Fly.io

---

**Happy testing!** 👻
