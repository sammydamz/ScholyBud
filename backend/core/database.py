"""Database initialization utilities."""

from sqlmodel import SQLModel

from backend.dependencies import engine


async def init_db() -> None:
    """Initialize database by creating all tables.

    This function should be called on application startup to ensure
    all database tables exist. It uses SQLAlchemy's create_all which
    is idempotent (safe to call multiple times).

    The function imports all model classes to ensure they are registered
    with SQLModel.metadata before creating tables.

    Example:
        On FastAPI startup event:
        @app.on_event("startup")
        async def on_startup():
            await init_db()
    """
    # Import all models to ensure they are registered with SQLModel.metadata
    from backend.models.school import School  # noqa: F401
    from backend.models.user import User  # noqa: F401
    from backend.models.student import Student, Class  # noqa: F401

    # Create all tables using run_sync for async engine
    # This is idempotent - safe to run multiple times
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
