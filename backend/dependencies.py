"""Common dependencies for FastAPI routes."""

from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from backend.config import settings

# Database engine
engine = create_async_engine(
    settings.test_database_url if settings.environment == "testing" else settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
)


async def dispose_engine() -> None:
    """Dispose the database engine for graceful shutdown.

    This function should be called in the FastAPI shutdown event handler:
        @app.on_event("shutdown")
        async def shutdown():
            await dispose_engine()
    """
    await engine.dispose()


async def get_session() -> AsyncSession:
    """Get database session dependency.

    Yields:
        AsyncSession: Database session for use in routes

    Example:
        @app.get("/users")
        async def list_users(session: Annotated[AsyncSession, Depends(get_session)]):
            result = await session.execute(select(User))
            return result.scalars().all()
    """
    async with AsyncSession(engine) as session:
        yield session


# Type alias for database session dependency
DBSessionDep = Annotated[AsyncSession, Depends(get_session)]

# Security scheme for JWT tokens
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    session: DBSessionDep,
) -> SQLModel | None:
    """Get current authenticated user from JWT token.

    This dependency extracts the JWT token from the Authorization header,
    validates it, and returns the authenticated user.

    Args:
        request: FastAPI request object
        credentials: HTTP Bearer credentials from Authorization header
        session: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found

    Note:
        This is a placeholder that will be fully implemented in Task 3.
        It imports from core.security and models.user once created.
    """
    # TODO: Implement in Task 3
    # from core.security import decode_token
    # from models.user import User

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # TODO: Decode token and get user from database
    # token = credentials.credentials
    # payload = decode_token(token)
    # user_id = payload.get("sub")
    # statement = select(User).where(User.id == user_id)
    # result = await session.execute(statement)
    # user = result.scalar_one_or_none()

    # if user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="User not found",
    #     )

    # return user

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User authentication not yet implemented - see Task 3"
    )


# Type alias for current user dependency
CurrentUserDep = Annotated[SQLModel, Depends(get_current_user)]


async def get_school_from_subdomain(request: Request, session: DBSessionDep) -> SQLModel | None:
    """Get school from subdomain in request Host header.

    Extracts the subdomain from the Host header and retrieves the
    corresponding school from the database.

    Args:
        request: FastAPI request object
        session: Database session

    Returns:
        School: The school object matching the subdomain

    Raises:
        HTTPException: If subdomain is invalid or school not found

    Note:
        This is a placeholder that will be fully implemented in Task 3.
        It imports from models.school once created.

    Example:
        For host: "school-a.scholybud.com"
        Subdomain: "school-a"
        Returns: School object for "school-a"
    """
    # TODO: Implement in Task 3
    # from models.school import School

    host = request.headers.get("host", "")

    # Extract subdomain from host using urlparse for robust parsing
    # Expected formats: {subdomain}.scholybud.com, localhost:{port}, 127.0.0.1:{port}
    if ":" in host:
        # Remove port number if present
        host = host.split(":")[0]

    parts = host.split(".")

    if len(parts) < 2 or host in ("localhost", "127", "0"):
        # For localhost or IP addresses, use a default school
        subdomain = "default"
    else:
        subdomain = parts[0]

    # TODO: Query school from database
    # statement = select(School).where(School.subdomain == subdomain)
    # result = await session.execute(statement)
    # school = result.scalar_one_or_none()

    # if school is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"School '{subdomain}' not found"
    #     )

    # return school

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="School lookup not yet implemented - see Task 3"
    )


# Type alias for school dependency
SchoolDep = Annotated[SQLModel, Depends(get_school_from_subdomain)]


async def get_optional_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    session: DBSessionDep,
) -> SQLModel | None:
    """Get current user if authenticated, otherwise return None.

    Similar to get_current_user but doesn't raise an exception if
    authentication fails. Useful for optional authentication.

    Args:
        credentials: HTTP Bearer credentials from Authorization header
        session: Database session

    Returns:
        User | None: The authenticated user or None

    Note:
        This is a placeholder that will be fully implemented in Task 3.
    """
    if credentials is None:
        return None

    # TODO: Implement in Task 3
    # from core.security import decode_token
    # from models.user import User
    # token = credentials.credentials
    # payload = decode_token(token)
    # user_id = payload.get("sub")
    # ... (get user from database)

    return None


# Type alias for optional current user dependency
OptionalCurrentUserDep = Annotated[SQLModel | None, Depends(get_optional_current_user)]
