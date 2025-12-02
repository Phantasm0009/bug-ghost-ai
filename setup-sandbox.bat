@echo off
REM Bug Ghost AI - Sandbox Setup Script for Windows
REM Builds all sandbox Docker images for local development

echo Building Bug Ghost AI Sandbox Images...
echo.

echo Building Python sandbox...
docker-compose build sandbox-python
if %errorlevel% neq 0 exit /b %errorlevel%

echo Building Node.js sandbox...
docker-compose build sandbox-node
if %errorlevel% neq 0 exit /b %errorlevel%

echo Building Java sandbox...
docker-compose build sandbox-java
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo All sandbox images built successfully!
echo.
echo Images created:
docker images | findstr bug-ghost-sandbox

echo.
echo You can now start the full stack with:
echo    docker-compose up -d
echo.
echo Test sandbox execution:
echo    curl -X POST http://localhost:8000/api/runs -H "Content-Type: application/json" -d "{\"language\": \"python\", \"code\": \"print('Hello from sandbox!')\"}"
echo.
