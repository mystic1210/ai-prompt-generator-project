#!/bin/bash
# Deployment script for development environment

set -e

echo "Deploying AI Prompt Generator SaaS..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "[ERROR] Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating .env file..."
    cp backend/.env.example backend/.env
fi

# Build and start containers
echo "Building Docker images..."
docker-compose -f deployment/docker-compose.yml build

echo "Starting services..."
docker-compose -f deployment/docker-compose.yml up -d

echo "Waiting for services to be ready..."
sleep 10

echo "[OK] Deployment complete!"
echo ""
echo "Services are running at:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Database: localhost:5432"
echo ""
echo "Default credentials (change in production):"
echo "   - Email: demo@promptgenerator.com"
echo "   - Password: (check backend/.env.example)"
echo ""
echo "💡 Useful commands:"
echo "   - View logs: docker-compose -f deployment/docker-compose.yml logs -f"
echo "   - Stop services: docker-compose -f deployment/docker-compose.yml down"
echo "   - Run migrations: docker-compose -f deployment/docker-compose.yml exec backend alembic upgrade head"
