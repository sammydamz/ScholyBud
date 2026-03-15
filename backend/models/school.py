from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Column, Field, JSON, SQLModel
from typing_extensions import Annotated


class School(SQLModel, table=True):
    """School model for multi-tenant isolation"""

    __tablename__ = "schools"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: Annotated[str, Field(max_length=255)]
    subdomain: Annotated[str, Field(max_length=100, unique=True, index=True)]
    logo_url: Optional[str] = Field(default=None, max_length=500)
    enabled_modules: list[str] = Field(
        sa_column=Column(JSON),
        default_factory=lambda: ["students", "attendance", "assessments", "fees"]
    )
    report_template: str = Field(default="classic", max_length=50)
    grading_system: dict = Field(sa_column=Column(JSON), default_factory=dict)
    academic_year: str = Field(default="2024/2025", max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)
