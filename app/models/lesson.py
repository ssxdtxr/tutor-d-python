from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.schemas.lesson import LessonStatusEnum


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))  # FK на students
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))  # UTC
    # ends_at вычисляется в сервисе: starts_at + duration_min
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration_min: Mapped[int]  # допустимые значения валидируются в схеме
    topic: Mapped[str] = mapped_column(String(200))
    status: Mapped[LessonStatusEnum] = mapped_column(
        Enum(LessonStatusEnum, native_enum=False),  # строка, не pg-тип ENUM
        default=LessonStatusEnum.planned,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # два знака после запятой
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # проставляет база
    )
