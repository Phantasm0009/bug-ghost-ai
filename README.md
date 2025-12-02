# Bug Ghost AI 👻🐛

**The AI Debug Replayer** - Transform error messages into reproducible bug scenarios with AI-powered analysis.

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

## 🚀 What is Bug Ghost AI?

Bug Ghost AI is an intelligent debugging assistant that turns your error messages into actionable insights. Simply paste an error, and our AI will:

- 🔍 **Analyze** the error and context
- ⚡ **Generate** minimal reproduction code
- 🧪 **Create** unit tests that trigger the bug
- 📝 **Explain** the root cause in plain English
- 🎯 **Suggest** a fix with code examples

Perfect for developers who want to:
- Quickly understand cryptic error messages
- Share reproducible bug reports with their team
- Learn from past debugging sessions
- Build a knowledge base of common errors

---

## ✨ Features

### Core Features (MVP)
- **Multi-language support**: JavaScript, TypeScript, Python, Java, Go, Rust, C++, C#, Ruby, PHP, and more
- **AI-powered analysis**: Uses GPT-4 or Claude to understand your error
- **Code generation**: Creates minimal reproduction scripts
- **Test generation**: Generates framework-appropriate unit tests (Jest, pytest, etc.)
- **Root cause analysis**: Explains what went wrong in plain English
- **Fix suggestions**: Provides actionable solutions
- **Session history**: View and revisit past debugging sessions
- **Beautiful UI**: Modern, responsive interface built with Next.js and Tailwind CSS

### Phase 2 Features (Now Available!) 🎉
- **Sandbox execution**: Run code in isolated Docker containers with strict security
- **Real-time log streaming**: Watch code execution via WebSocket
- **Multi-language runtime**: Python, Node.js, Java support out of the box
- **Security hardened**: Non-root execution, no network, resource limits
- **Docker-in-Docker**: Easy deployment with full stack in Compose

### Planned Features (Phase 3)
- **Sandbox execution**: Run reproductions in isolated Docker containers
- **Live debugging**: Step through reproduction code
- **Team collaboration**: Share sessions with teammates
- **GitHub integration**: Create issues directly from sessions
- **Custom LLM models**: Support for local/custom AI models

---

## 🏗️ Architecture

```
bug-ghost-ai/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── api/         # REST API routes
│   │   ├── models/      # SQLAlchemy database models
│   │   ├── schemas/     # Pydantic validation schemas
│   │   ├── services/    # Business logic (LLM, reproduction generation)
│   │   └── db/          # Database configuration
│   └── tests/           # Backend unit tests
│
├── frontend/            # Next.js 14 frontend
│   ├── app/            # App Router pages
│   ├── components/     # React components
│   └── lib/            # Utilities and API client
│
└── docker-compose.yml  # Full stack orchestration
```

### Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- React Hook Form
- Tailwind CSS
- Axios
- Lucide Icons

**Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy + PostgreSQL
- Pydantic
- OpenAI / Anthropic SDKs

**Infrastructure:**
- Docker & Docker Compose
- Docker-in-Docker (DinD) for safe code execution
- PostgreSQL 15
- Nginx (optional)

---

## 🛠️ Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+ (or use Docker)
- **OpenAI API key** or **Anthropic API key**

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bug-ghost-ai.git
   cd bug-ghost-ai
   ```

2. **Set up environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your API key

   # Frontend
   cp frontend/.env.example frontend/.env.local
   ```

3. **Build sandbox images** (first time only)
   ```bash
   # Linux/Mac
   chmod +x setup-sandbox.sh
   ./setup-sandbox.sh
   
   # Windows
   setup-sandbox.bat
   
   # Or manually
   docker-compose build sandbox-python sandbox-node sandbox-java
   ```

4. **Start all services**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # OR using Poetry
   poetry install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bug_ghost_ai
   LLM_PROVIDER=openai
   LLM_API_KEY=your-api-key-here
   LLM_MODEL=gpt-4-turbo-preview
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb bug_ghost_ai
   
   # Tables will be created automatically on first run
   ```

6. **Run the backend**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Edit `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the frontend**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   - Visit http://localhost:3000

---

## 📖 Usage Guide

### Creating Your First Debug Session

1. **Select Language**: Choose the programming language of your error
2. **Add Runtime Info** (optional): Specify version (e.g., "Node 18", "Python 3.11")
3. **Paste Error**: Copy your error message or stack trace
4. **Add Code Snippet** (recommended): Include the relevant code
5. **Provide Context** (optional): Describe when the error occurs
6. **Submit**: Click "Generate Reproduction"

### Viewing Results

The AI will generate:
- **Root Cause**: Explanation of what went wrong
- **Fix Suggestion**: How to resolve the issue
- **Repro Code**: Minimal code to reproduce the bug
- **Test Code**: Unit test that triggers the error
- **Original Context**: Your input for reference

### Managing Sessions

- View all past sessions at `/sessions`
- Click any session to see full details
- Share session URLs with teammates

---

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Type Checking
```bash
cd frontend
npm run type-check
```

---

## 🔧 Configuration

### LLM Provider Options

#### OpenAI (Default)
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4-turbo-preview
```

#### Anthropic Claude
```env
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-...
LLM_MODEL=claude-3-opus-20240229
```

### Database Configuration

PostgreSQL connection string format:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

### CORS Configuration

Update `backend/app/config.py`:
```python
CORS_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com"
]
```

---

## 🚢 Deployment

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables for Production

Backend:
- `DATABASE_URL`: Production PostgreSQL URL
- `LLM_API_KEY`: Your API key
- `CORS_ORIGINS`: Your frontend domain(s)

Frontend:
- `NEXT_PUBLIC_API_URL`: Your backend API URL

### Recommended Platforms

- **Frontend**: Vercel, Netlify
- **Backend**: Railway, Render, DigitalOcean App Platform
- **Database**: Supabase, Neon, AWS RDS

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style
- Write tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📝 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Create Debug Session
```http
POST /api/debug-sessions
Content-Type: application/json

{
  "language": "javascript",
  "runtime_info": "Node 18",
  "error_text": "TypeError: Cannot read property 'x' of undefined",
  "code_snippet": "const obj = {};\nconsole.log(obj.x.y);",
  "context_description": "Happens when clicking submit button"
}
```

#### Get Session
```http
GET /api/debug-sessions/{session_id}
```

#### List Sessions
```http
GET /api/debug-sessions?skip=0&limit=20
```

#### Execute Code in Sandbox (Phase 2)
```http
POST /api/runs
Content-Type: application/json

{
  "language": "python",
  "code": "print('Hello from sandbox!')\nfor i in range(5):\n    print(f'Count: {i}')",
  "timeout_sec": 10
}
```

Response:
```json
{
  "run_id": "550e8400-e29b-41d4-a716-446655440000",
  "language": "python",
  "status": "completed",
  "stdout": "Hello from sandbox!\nCount: 0\nCount: 1\nCount: 2\nCount: 3\nCount: 4\n",
  "image": "bug-ghost-sandbox-python:latest",
  "created_at": "2025-12-01T10:30:00Z"
}
```

#### Stream Run Logs (WebSocket)
```javascript
const ws = new WebSocket('ws://localhost:8000/api/runs/ws/{run_id}/logs');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data.data); // stdout, stderr, or complete
};
```

---

## 🔒 Sandbox Security

The sandbox execution system implements multiple security layers:

- **Isolation**: Each run in a fresh, isolated container
- **Non-root**: Code runs as user `1000:1000` (not root)
- **No network**: `network_disabled=True` by default
- **Resource limits**: 256MB RAM, ~50% CPU quota
- **Time limits**: 10-60 second execution timeout
- **No persistence**: Container destroyed after execution
- **Code injection**: No host mounts; code via in-memory tar

Supported languages: Python, Node.js (JavaScript/TypeScript), Java

---

## 🎯 Roadmap

### MVP (Current) ✅
- [x] Error submission form
- [x] AI-powered reproduction generation
- [x] Session history
- [x] Multi-language support
- [x] Beautiful UI

### Phase 2 (Current) ✅
- [x] Docker sandbox execution
- [x] Real-time log streaming (WebSocket)
- [x] Security-hardened containers
- [x] Multi-language runtime support
- [ ] Team collaboration
- [ ] GitHub integration

### Phase 3 (Q3 2025)
- [ ] Custom LLM model support
- [ ] Advanced analytics
- [ ] Browser extension
- [ ] VS Code extension
- [ ] Slack/Discord integration

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Built with ❤️ by developers, for developers
- Powered by OpenAI GPT-4 and Anthropic Claude
- Inspired by the frustration of debugging cryptic errors

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bug-ghost-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bug-ghost-ai/discussions)
- **Twitter**: [@BugGhostAI](https://twitter.com/BugGhostAI)
- **Email**: support@bugghost.ai

---

## ⭐ Star History

If you find Bug Ghost AI helpful, please consider giving it a star!

---

**Made with 👻 by the Bug Ghost AI team**
