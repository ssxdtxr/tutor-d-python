from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LessonStatusEnum(StrEnum):
    planned = "planned"
    done = "done"
    cancelled = "cancelled"


# Тело POST-запроса — статус не передаётся, всегда planned
class LessonCreate(BaseModel):
    student_id: int
    starts_at: datetime
    duration_min: Literal[30, 45, 60, 90]
    topic: str = Field(min_length=1, max_length=200)
    price: Decimal = Field(ge=0, le=100000, decimal_places=2)

    @field_validator("starts_at")
    @classmethod
    def must_have_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("starts_at must include timezone")
        return v


# Тело PATCH-запроса — все поля опциональны
class LessonUpdate(BaseModel):
    student_id: int | None = None
    starts_at: datetime | None = None
    duration_min: Literal[30, 45, 60, 90] | None = None
    topic: str | None = Field(default=None, min_length=1, max_length=200)
    price: Decimal | None = Field(default=None, ge=0, le=100000, decimal_places=2)
    status: LessonStatusEnum | None = None

    @field_validator("starts_at")
    @classmethod
    def must_have_timezone(cls, v: datetime | None) -> datetime | None:
        # None означает "не менять", пропускаем
        if v is not None and v.tzinfo is None:
            raise ValueError("starts_at must include timezone")
        return v


# Ответ API — все поля включая вычисленные ends_at и created_at
class LessonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    starts_at: datetime
    ends_at: datetime
    duration_min: int
    topic: str
    status: LessonStatusEnum
    price: Decimal
    created_at: datetime
