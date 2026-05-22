#!/bin/bash
# Quick setup script for Windows (using WSL or Git Bash)

set -e

echo "AI Prompt Generator SaaS - Quick Setup"
echo "========================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker not found. Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo "[ERROR] Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo "[OK] Docker and Docker Compose found"
echo ""

# Create .env if not exists
echo "Setting up environment..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "[OK] Created backend/.env"
fi

# Build and start
echo "Building and starting services..."
docker compose -f deployment/docker-compose.yml build
docker compose -f deployment/docker-compose.yml up -d

echo "Waiting for services to start..."
sleep 10

# Check services
echo ""
echo "[OK] Deployment successful!"
echo ""
echo "Access the application:"
echo "   Frontend:        http://localhost:3000"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   Database:        localhost:5432"
echo ""
echo "Test Credentials:"
echo "   Email:    demo@promptgenerator.com"
echo "   Password: (check backend/.env)"
echo ""
echo "Useful commands:"
echo "   View logs:       docker logs -f prompt_generator_backend"
echo "   Stop services:   docker compose -f deployment/docker-compose.yml down"
echo "   Restart:         docker compose -f deployment/docker-compose.yml restart"
echo ""
echo "Full documentation in SAAS_README.md"
