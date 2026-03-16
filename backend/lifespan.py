"""Application lifespan manager for FastAPI.

This module provides the lifespan context manager that handles
startup and shutdown events for the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.database import init_db
from backend.dependencies import dispose_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.

    This context manager handles startup and shutdown operations for the FastAPI application.
    On startup, it initializes the database. On shutdown, it disposes the database engine
    for graceful shutdown.

    Args:
        app: The FastAPI application instance

    Yields:
        None: Control is yielded to the application during its lifetime

    Example:
        app = FastAPI(lifespan=lifespan)
    """
    # Startup: Initialize database
    await init_db()

    yield

    # Shutdown: Dispose database engine for graceful shutdown
    await dispose_engine()
