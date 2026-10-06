from enum import StrEnum

from pydantic import BaseModel, Field


class StudentLevelEnum(StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=6, le=18)
    grade: int = Field(ge=1, le=11)
    level: StudentLevelEnum = StudentLevelEnum.beginner
    parent_contact: str | None = Field(default=None, max_length=100)


class StudentSchema(StudentBase):
    id: str


class StudentCreateSchema(StudentBase):
    pass


class StudentUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=6, le=18)
    grade: int | None = Field(default=None, ge=1, le=11)
    level: StudentLevelEnum | None = None
    parent_contact: str | None = Field(default=None, max_length=100)
