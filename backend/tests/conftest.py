"""Pytest configuration and fixtures for ScholyBud tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel

from backend.main import app
from backend.dependencies import engine
from backend.models import School, User


@pytest.fixture
async def client():
    """Async HTTP client for testing FastAPI endpoints.

    Yields:
        AsyncClient: HTTP client configured to test the FastAPI app
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Create and tear down test database tables.

    This fixture creates all tables before each test and drops them after.

    Yields:
        None: Tables are created before yield, dropped after
    """
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
