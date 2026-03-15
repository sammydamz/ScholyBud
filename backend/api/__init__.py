"""Backend API routers module.

This module exports all API routers for the ScholyBud backend application.
Each router is organized by feature/domain (auth, users, schools, etc.).
"""

from backend.api.auth import auth_router

__all__ = ["auth_router"]
