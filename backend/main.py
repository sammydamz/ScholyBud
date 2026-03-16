"""Main FastAPI application for ScholyBud.

This module initializes and configures the FastAPI application with all
necessary middleware, routers, and lifecycle handlers.
"""

from typing import TypedDict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import auth_router
from backend.config import settings
from backend.lifespan import lifespan


class RootResponse(TypedDict):
    """Response type for the root endpoint."""
    message: str
    version: str
    docs: str


class HealthResponse(TypedDict):
    """Response type for the health check endpoint."""
    status: str


# Create FastAPI application
app = FastAPI(
    title="ScholyBud API",
    description="School Management System API",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    """Root endpoint providing API information.

    Returns:
        RootResponse: Dictionary containing API message, version, and docs URL
    """
    return {
        "message": "ScholyBud API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint.

    Returns:
        HealthResponse: Dictionary containing the health status
    """
    return {"status": "healthy"}
