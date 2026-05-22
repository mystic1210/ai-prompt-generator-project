version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: prompt_generator_db
    environment:
      POSTGRES_USER: promptgenerator
      POSTGRES_PASSWORD: password
      POSTGRES_DB: prompt_generator_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
      - ./database/sample_data.sql:/docker-entrypoint-initdb.d/02-sample_data.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U promptgenerator"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: .
      dockerfile: deployment/Dockerfile.backend
    container_name: prompt_generator_backend
    environment:
      DATABASE_URL: postgresql://promptgenerator:password@postgres:5432/prompt_generator_db
      SECRET_KEY: your-super-secret-key-change-in-production
      ENVIRONMENT: development
      DEBUG: "true"
      CORS_ORIGINS: '["http://localhost:3000","http://localhost:8000"]'
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: .
      dockerfile: deployment/Dockerfile.frontend
    container_name: prompt_generator_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      VITE_API_URL: http://backend:8000

  # Nginx Reverse Proxy (optional)
  nginx:
    image: nginx:alpine
    container_name: prompt_generator_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deployment/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:

networks:
  default:
    name: prompt_generator_network
