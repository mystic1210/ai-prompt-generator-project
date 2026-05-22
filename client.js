#!/bin/bash
# Production deployment script

set -e

echo "Production Deployment"
echo "========================"

# Configuration
ENVIRONMENT=${ENVIRONMENT:-production}
DOCKER_REGISTRY=${DOCKER_REGISTRY:-docker.io}
IMAGE_NAME=${IMAGE_NAME:-prompt-generator}
VERSION=${VERSION:-$(git describe --tags --always)}

echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"
echo ""

# Build images
echo "Building Docker images..."
docker build -t $DOCKER_REGISTRY/$IMAGE_NAME-backend:$VERSION -f deployment/Dockerfile.backend .
docker build -t $DOCKER_REGISTRY/$IMAGE_NAME-frontend:$VERSION -f deployment/Dockerfile.frontend .

# Push to registry (if credentials provided)
if [ ! -z "$DOCKER_USERNAME" ]; then
    echo "Pushing images to registry..."
    docker push $DOCKER_REGISTRY/$IMAGE_NAME-backend:$VERSION
    docker push $DOCKER_REGISTRY/$IMAGE_NAME-frontend:$VERSION
fi

echo "[OK] Build complete!"
echo ""
echo "Images built:"
echo "   - Backend: $DOCKER_REGISTRY/$IMAGE_NAME-backend:$VERSION"
echo "   - Frontend: $DOCKER_REGISTRY/$IMAGE_NAME-frontend:$VERSION"
