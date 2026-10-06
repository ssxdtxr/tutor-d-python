from enum import Enum

from pydantic import BaseModel, Field


class StudentLevelEnum(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class StudentSchema(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=6, le=18)
    grade: int = Field(ge=1, le=11)
    level: StudentLevelEnum = Field(default=StudentLevelEnum.beginner)
    parent_contact: str | None = Field(max_length=100)


class StudentReadSchema(BaseModel):
    id: str
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=6, le=18)
    grade: int = Field(ge=1, le=11)
    level: StudentLevelEnum = Field(default=StudentLevelEnum.beginner)
    parent_contact: str | None = Field(max_length=100)


class StudentCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=6, le=18)
    grade: int = Field(ge=1, le=11)
    level: StudentLevelEnum = Field(default=StudentLevelEnum.beginner)
    parent_contact: str | None = Field(max_length=100)


class StudentUpdateSchema(BaseModel):
    name: str | None = Field(min_length=1, max_length=100)
    age: int | None = Field(ge=6, le=18)
    grade: int | None = Field(ge=1, le=11)
    level: StudentLevelEnum = Field(default=StudentLevelEnum.beginner)
    parent_contact: str | None = Field(max_length=100)
