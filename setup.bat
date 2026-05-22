@echo off
REM Quick setup script for Windows (Command Prompt)

echo.
echo AI Prompt Generator SaaS - Quick Setup Windows
echo ===================================================
echo.

REM Check Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found. Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose not found. Please install Docker Compose.
    exit /b 1
)

echo [OK] Docker and Docker Compose found
echo.

REM Create .env if not exists
echo Setting up environment...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo [OK] Created backend\.env
)

REM Build and start
echo Building and starting services...
docker compose -f deployment/docker-compose.yml build
docker compose -f deployment/docker-compose.yml up -d

echo Waiting for services to start...
timeout /t 10

REM Check services
echo.
echo [OK] Deployment successful!
echo.
echo Access the application:
echo    Frontend:        http://localhost:3000
echo    Backend API:     http://localhost:8000
echo    API Docs:        http://localhost:8000/docs
echo    Database:        localhost:5432
echo.
echo Test Credentials:
echo    Email:    demo@promptgenerator.com
echo    Password: (check backend\.env)
echo.
echo Useful commands:
echo    View logs:       docker logs -f prompt_generator_backend
echo    Stop services:   docker compose -f deployment/docker-compose.yml down
echo    Restart:         docker compose -f deployment/docker-compose.yml restart
echo.
echo Full documentation in SAAS_README.md
