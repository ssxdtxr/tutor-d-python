from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StudentLevelEnum(StrEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# Общие поля и валидация — база для Create и Schema
class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=6, le=18)
    grade: int = Field(ge=1, le=11)
    level: StudentLevelEnum = StudentLevelEnum.beginner
    parent_contact: str | None = Field(default=None, max_length=100)


# Ответ API — содержит id.
# from_attributes=True — читает данные из ORM-объекта через атрибуты, не словарь
class StudentSchema(StudentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Тело POST-запроса — id не нужен, его выдаёт база
class StudentCreateSchema(StudentBase):
    pass


# Тело PATCH-запроса — все поля опциональны (частичное обновление).
# Валидатор запрещает явно передавать null для обязательных полей.
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
