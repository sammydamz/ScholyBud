from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel
from typing_extensions import Annotated, Literal

from backend.core.security import get_password_hash, verify_password


class UserRole:
    """User role constants"""
    SUPER_ADMIN = "super_admin"
    SCHOOL_ADMIN = "school_admin"
    TEACHER = "teacher"


class User(SQLModel, table=True):
    """User model for authentication"""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: Annotated[str, Field(max_length=255, unique=True, index=True)]
    password_hash: Annotated[str, Field(max_length=255)]
    role: Literal["super_admin", "school_admin", "teacher"] = Field(default="teacher")
    school_id: Optional[UUID] = Field(default=None, foreign_key="schools.id")
    first_name: Annotated[str, Field(max_length=100)]
    last_name: Annotated[str, Field(max_length=100)]
    phone: Optional[str] = Field(default=None, max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password"""
        self.password_hash = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return verify_password(password, self.password_hash)
