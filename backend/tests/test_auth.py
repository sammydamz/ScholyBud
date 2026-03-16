"""Tests for authentication endpoints."""

import pytest


@pytest.mark.asyncio
async def test_register_success(client, test_db):
    """Test successful user registration."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, test_db):
    """Test registration with duplicate email fails."""
    # First registration
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }
    )

    # Duplicate registration
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "DifferentPassword123!",
            "first_name": "Another",
            "last_name": "User",
        }
    )

    assert response.status_code == 400
    data = response.json()
    assert "already registered" in data["detail"].lower()


@pytest.mark.asyncio
async def test_login_success(client, test_db):
    """Test successful login returns access token."""
    # Register user first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "TestPassword123!",
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, test_db):
    """Test login with invalid credentials fails."""
    response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "WrongPassword123!",
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_unauthorized(client, test_db):
    """Test getting current user without authentication fails."""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authorized(client, test_db):
    """Test getting current user with authentication succeeds."""
    # Register user
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
        }
    )

    # Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "TestPassword123!",
        }
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
