@echo off
echo Setting up Bug Ghost AI...

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.11+
    exit /b 1
)

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js not found. Please install Node.js 18+
    exit /b 1
)

echo Prerequisites check complete

REM Setup backend
echo.
echo Setting up backend...
cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    copy .env.example .env
    echo Please edit backend\.env with your API keys
)

cd ..
echo Backend setup complete

REM Setup frontend
echo.
echo Setting up frontend...
cd frontend

REM Install dependencies
call npm install

REM Copy environment file
if not exist .env.local (
    copy .env.example .env.local
)

cd ..
echo Frontend setup complete

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your LLM API key
echo 2. Create PostgreSQL database (or use Docker Compose)
echo 3. Start backend: cd backend ; .\venv\Scripts\activate ; uvicorn app.main:app --reload
echo 4. Start frontend: cd frontend ; npm run dev
echo.
echo Or use Docker Compose: docker-compose up
echo.
