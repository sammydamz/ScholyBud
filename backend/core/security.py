"""Security utilities for JWT tokens and password hashing."""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.config import settings

# CryptContext singleton for password hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token.

    Args:
        data: Payload data to encode in the token (typically {"sub": user_id})
        expires_delta: Optional custom expiration time. Defaults to settings.access_token_expire_minutes

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token(data={"sub": "user_id"})
        >>> # Token expires in 7 days by default
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload if valid, None if invalid

    Example:
        >>> payload = decode_token(token)
        >>> if payload:
        ...     user_id = payload.get("sub")
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if passwords match, False otherwise

    Example:
        >>> is_valid = verify_password("user_password", hashed_password_from_db)
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Example:
        >>> hashed = get_password_hash("user_password")
        >>> # Store hashed password in database
    """
    return pwd_context.hash(password)
