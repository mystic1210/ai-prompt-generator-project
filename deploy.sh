"""Main FastAPI application"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, prompts
from app.database import Base, engine
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-Grade AI Prompt Generator SaaS API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# API Info endpoint
@app.get("/api/info")
def api_info():
    """Get API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(prompts.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Prompt Generator SaaS API",
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
