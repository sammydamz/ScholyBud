from datetime import datetime, date, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship
from typing_extensions import Annotated, Literal


class Gender:
    """Gender constants"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class StudentStatus:
    """Student status constants"""
    ACTIVE = "active"
    GRADUATED = "graduated"
    WITHDRAWN = "withdrawn"
    TRANSFERRED = "transferred"
    SUSPENDED = "suspended"


class Class(SQLModel, table=True):
    """Class model for organizing students"""

    __tablename__ = "classes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    school_id: UUID = Field(foreign_key="schools.id")
    name: Annotated[str, Field(max_length=100)]
    level: Annotated[str, Field(max_length=50)]
    class_teacher_id: Optional[UUID] = Field(default=None, foreign_key="users.id")
    capacity: int = Field(default=40)
    academic_year: Annotated[str, Field(max_length=20)]
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Student(SQLModel, table=True):
    """Student model"""

    __tablename__ = "students"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    school_id: UUID = Field(foreign_key="schools.id")
    admission_number: Annotated[str, Field(max_length=50, unique=True, index=True)]
    first_name: Annotated[str, Field(max_length=100)]
    last_name: Annotated[str, Field(max_length=100)]
    other_names: Optional[str] = Field(default=None, max_length=100)
    date_of_birth: date
    gender: Literal["male", "female", "other"]
    guardian_name: Annotated[str, Field(max_length=200)]
    guardian_phone: Annotated[str, Field(max_length=20)]
    guardian_email: Optional[str] = Field(default=None, max_length=255)
    guardian_relationship: Annotated[str, Field(max_length=50)]
    address: Annotated[str, Field(max_length=500)]
    class_id: Optional[UUID] = Field(default=None, foreign_key="classes.id")
    status: Literal["active", "graduated", "withdrawn", "transferred", "suspended"] = Field(
        default="active"
    )
    photo_url: Optional[str] = Field(default=None, max_length=500)
    enrollment_date: date
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
