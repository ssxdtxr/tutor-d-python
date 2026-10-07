from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


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
    id: int


class StudentCreateSchema(StudentBase):
    pass


class StudentUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=6, le=18)
    grade: int | None = Field(default=None, ge=1, le=11)
    level: StudentLevelEnum | None = None
    parent_contact: str | None = Field(default=None, max_length=100)

    @model_validator(mode="after")
    def required_fields_not_null(self):
        if "age" in self.model_fields_set and self.age is None:
            raise ValueError("age не может быть null")
        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("name не может быть null")
        if "grade" in self.model_fields_set and self.grade is None:
            raise ValueError("grade не может быть null")
        return self
