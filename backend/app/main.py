"""
FastAPI Application Entry Point for SOC Alert Triage System
"""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router
from app.middleware.error_handler import ErrorHandlerMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Application startup: Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Application shutdown")


# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="Security Operations Center Alert Triage System",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(ErrorHandlerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, Any]:
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "0.1.0"
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict[str, Any]:
    """
    Root endpoint with API information
    """
    return {
        "message": "SOC Alert Triage System API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception) -> JSONResponse:
    """
    Global exception handler
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )