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
    parent_contact: str | None = Field(max_length=100)


class StudentSchema(StudentBase):
    id: str


class StudentCreateSchema(StudentBase):
    pass


class StudentUpdateSchema(BaseModel):
    name: str | None = Field(min_length=1, max_length=100)
    age: int | None = Field(ge=6, le=18)
    grade: int | None = Field(ge=1, le=11)
    level: StudentLevelEnum | None = None
    parent_contact: str | None = Field(max_length=100)
