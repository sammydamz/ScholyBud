"""Authentication API endpoints for user registration, login, and token management."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from backend.config import settings
from backend.core.security import create_access_token
from backend.dependencies import DBSessionDep, get_current_user
from backend.models.user import User
from backend.schemas.auth import RegisterRequest, Token
from backend.schemas.user import UserResponse


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    session: DBSessionDep,
) -> User:
    """Register a new user.

    Args:
        user_data: Registration data including email, password, and name
        session: Database session

    Returns:
        UserResponse: Created user object

    Raises:
        HTTPException: If email already exists (400)
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    result = await session.exec(statement)
    existing_user = result.one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user with default role
    from backend.core.security import get_password_hash
    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=get_password_hash(user_data.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@auth_router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DBSessionDep,
) -> Token:
    """Authenticate user and return JWT access token.

    Uses OAuth2PasswordRequestForm for form-based authentication.
    Accepts 'username' (email) and 'password' as form fields.

    Args:
        form_data: OAuth2 form with username (email) and password
        session: Database session

    Returns:
        Token response with access_token and token_type

    Raises:
        HTTPException: If credentials invalid (401), user inactive (403)
    """
    # Find user by email (username field)
    statement = select(User).where(User.email == form_data.username)
    result = await session.exec(statement)
    user = result.one_or_none()

    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create JWT token with user claims
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
            "school_id": str(user.school_id) if user.school_id else None,
        },
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token)


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current authenticated user information.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        UserResponse: Current user object
    """
    return current_user


@auth_router.post("/logout")
async def logout() -> dict[str, str]:
    """Logout current user.

    Client-side token removal is recommended for proper logout.
    This endpoint returns a success message for client handling.

    Returns:
        Success message

    Note:
        JWT tokens are stateless and cannot be invalidated server-side
        without a token blacklist. Best practice is to remove the token
        from client storage (localStorage, cookies, etc.).
    """
    return {"message": "Successfully logged out"}
