from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    """User response schema."""

    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: Literal["super_admin", "school_admin", "teacher"]
    school_id: UUID | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None


class UserCreate(BaseModel):
    """Create user request schema."""

    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    role: Literal["super_admin", "school_admin", "teacher"]
    phone: str | None = Field(default=None, max_length=20)
