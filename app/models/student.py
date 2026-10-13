from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.schemas.student import StudentLevelEnum


# Описание сущности в таблице БД
class Student(Base):
    __tablename__ = "students"  # имя таблицы в PostgreSQL

    id: Mapped[int] = mapped_column(primary_key=True)  # id выдаёт база
    name: Mapped[str] = mapped_column(String(100))  # совпадает с Pydantic-валидацией
    age: Mapped[int]
    grade: Mapped[int]
    level: Mapped[StudentLevelEnum] = mapped_column(
        Enum(StudentLevelEnum, native_enum=False)  # строка, не pg-тип ENUM
    )
    parent_contact: Mapped[str | None] = mapped_column(String(100))  # None → NULL в БД

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),    # TIMESTAMPTZ — хранит часовой пояс
        server_default=func.now()   # время проставляет база, не приложение
    )
