from datetime import date, datetime
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    """Create student request schema."""

    admission_number: Annotated[str, Field(min_length=1, max_length=50)]
    first_name: Annotated[str, Field(min_length=1, max_length=100)]
    last_name: Annotated[str, Field(min_length=1, max_length=100)]
    other_names: str | None = Field(default=None, max_length=100)
    date_of_birth: date
    gender: Annotated[Literal["male", "female", "other"], Field(pattern="^(male|female|other)$")]
    guardian_name: Annotated[str, Field(min_length=1, max_length=255)]
    guardian_phone: Annotated[str, Field(min_length=10, max_length=20)]
    guardian_email: EmailStr | None = Field(default=None, max_length=255)
    guardian_relationship: Annotated[str, Field(max_length=50)] = Field(default="Parent")
    address: Annotated[str, Field(min_length=1, max_length=500)]
    class_id: UUID | None = Field(default=None)
    photo_url: str | None = Field(default=None, max_length=500)


class StudentUpdate(BaseModel):
    """Update student request schema."""

    first_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    other_names: str | None = Field(default=None, max_length=100)
    guardian_name: Annotated[str, Field(min_length=1, max_length=255)] | None = None
    guardian_phone: Annotated[str, Field(min_length=10, max_length=20)] | None = None
    guardian_email: EmailStr | None = Field(default=None, max_length=255)
    guardian_relationship: Annotated[str, Field(max_length=50)] | None = None
    address: Annotated[str, Field(min_length=1, max_length=500)] | None = None
    class_id: UUID | None = Field(default=None)
    photo_url: str | None = Field(default=None, max_length=500)
    status: Literal["active", "graduated", "withdrawn", "transferred", "suspended"] | None = None


class StudentResponse(BaseModel):
    """Student response schema."""

    id: UUID
    school_id: UUID
    admission_number: str
    first_name: str
    last_name: str
    other_names: str | None
    date_of_birth: date
    gender: Literal["male", "female", "other"]
    guardian_name: str
    guardian_phone: str
    guardian_email: str | None
    guardian_relationship: str
    address: str
    class_id: UUID | None
    status: Literal["active", "graduated", "withdrawn", "transferred", "suspended"]
    photo_url: str | None
    enrollment_date: date
    created_at: datetime
    updated_at: datetime | None


class StudentListResponse(BaseModel):
    """Paginated student list response schema."""

    total: int
    students: list[StudentResponse]
    offset: int
    limit: int
