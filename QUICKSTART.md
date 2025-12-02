# Bug Ghost AI - Quick Start Guide

Get up and running with Bug Ghost AI in under 5 minutes! 🚀

## Prerequisites

- **Docker & Docker Compose** (easiest option)
  
  OR
  
- **Node.js** 18+
- **Python** 3.11+
- **PostgreSQL** 15+

## Option 1: Docker Compose (Recommended) 🐳

This is the fastest way to get started!

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/bug-ghost-ai.git
cd bug-ghost-ai
```

### 2. Set up environment variables

**Backend:**
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and add your LLM API key:
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-actual-api-key-here
LLM_MODEL=gpt-4-turbo-preview
```

**Frontend:**
```bash
cd ../frontend
cp .env.example .env.local
```

The default values should work for local development.

### 3. Start everything
```bash
cd ..
docker-compose up
```

Wait for all services to start (about 30-60 seconds).

### 4. Open your browser
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Try it out!

1. Go to http://localhost:3000
2. Select a programming language
3. Paste an error message
4. Add some code (optional)
5. Click "Generate Reproduction"
6. Watch the AI analyze your error! ✨

---

## Option 2: Manual Setup 🛠️

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/bug-ghost-ai.git
cd bug-ghost-ai
```

### 2. Set up PostgreSQL

Create a new database:
```bash
createdb bug_ghost_ai
```

Or use Docker just for PostgreSQL:
```bash
docker run -d \
  --name bug-ghost-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bug_ghost_ai \
  -p 5432:5432 \
  postgres:15-alpine
```

### 3. Set up the backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bug_ghost_ai
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-actual-api-key-here
LLM_MODEL=gpt-4-turbo-preview
```

Start the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Set up the frontend

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start the frontend:
```bash
npm run dev
```

### 5. Open your browser
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs

---

## Using Setup Scripts

We've provided automated setup scripts!

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```batch
setup.bat
```

These scripts will:
- Create virtual environments
- Install dependencies
- Copy environment files
- Show next steps

---

## Getting Your API Key

### OpenAI (Recommended for MVP)

1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste into `backend/.env`

**Recommended model:** `gpt-4-turbo-preview`

### Anthropic Claude

1. Go to https://console.anthropic.com/
2. Sign in or create account
3. Navigate to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-`)
6. Update `backend/.env`:
   ```env
   LLM_PROVIDER=anthropic
   LLM_API_KEY=sk-ant-your-key-here
   LLM_MODEL=claude-3-opus-20240229
   ```

---

## Example Usage

### Example 1: JavaScript Error

**Input:**
```
Language: JavaScript
Runtime: Node 18

Error:
TypeError: Cannot read property 'name' of undefined
  at getUserName (users.js:10:15)
  at main.js:5:12

Code:
function getUserName(user) {
  return user.profile.name;
}
```

**AI Output:**
- Minimal reproduction code
- Jest test case
- Explanation of null/undefined access
- Fix using optional chaining

### Example 2: Python Error

**Input:**
```
Language: Python
Runtime: Python 3.11

Error:
AttributeError: 'NoneType' object has no attribute 'get'

Code:
response = api_call()
data = response.get('data')
```

**AI Output:**
- Reproduction script
- Pytest test
- Explanation of None handling
- Fix with proper None checking

---

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError`
```bash
# Make sure you activated the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Error:** `Database connection failed`
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env
# Make sure database exists
createdb bug_ghost_ai
```

**Error:** `LLM API error`
- Verify your API key is correct in `.env`
- Check you have credits/quota
- Try with a different model

### Frontend won't start

**Error:** `Module not found`
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Error:** `Can't connect to API`
- Check backend is running on port 8000
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

### Docker issues

**Error:** `Port already in use`
```bash
# Stop existing services
docker-compose down

# Check what's using the port
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill the process or change ports in docker-compose.yml
```

**Error:** `Build failed`
```bash
# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

---

## Next Steps

1. ✅ **Try the demo** - Submit a few errors
2. 📖 **Read the docs** - Check out `README.md` and `DEVELOPER_GUIDE.md`
3. 🔧 **Customize** - Adjust prompts, add features
4. 🚀 **Deploy** - Use the deployment guides
5. 🤝 **Contribute** - See `CONTRIBUTING.md`

---

## Quick Commands Reference

### Docker Compose
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose build
```

### Backend
```bash
# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Run server
uvicorn app.main:app --reload

# Run tests
pytest

# Check coverage
pytest --cov=app
```

### Frontend
```bash
# Development
npm run dev

# Production build
npm run build
npm start

# Type check
npm run type-check

# Linting
npm run lint
```

---

## Support

Need help?
- 📖 Check `README.md` for detailed docs
- 🐛 Open an issue on GitHub
- 💬 Join our discussions
- 📧 Email: support@bugghost.ai

---

**Happy Debugging! 👻🐛**
