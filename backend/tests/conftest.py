"""Pytest configuration and fixtures for ScholyBud tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.config import settings
from backend.dependencies import get_session
from backend.main import app


@pytest.fixture
async def test_db():
    """Create and tear down test database tables using a dedicated test engine.

    This fixture creates all tables before each test and drops them after,
    using the test database URL to avoid touching the development database.
    It also overrides the app's session dependency to use the test engine.

    Yields:
        None: Tables are created before yield, dropped after
    """
    test_engine = create_async_engine(settings.test_database_url, echo=False)

    # Import all models to register them with SQLModel.metadata
    from backend.models.school import School  # noqa: F401
    from backend.models.user import User  # noqa: F401
    from backend.models.student import Student, Class  # noqa: F401

    # Override session dependency to use test engine
    async def override_get_session():
        async with AsyncSession(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Drop all tables and clean up
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    app.dependency_overrides.pop(get_session, None)
    await test_engine.dispose()


@pytest.fixture
async def client(test_db):
    """Async HTTP client for testing FastAPI endpoints.

    Depends on test_db to ensure the test engine and session overrides
    are in place before any requests are made.

    Yields:
        AsyncClient: HTTP client configured to test the FastAPI app
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
