from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.schemas.student import StudentLevelEnum


class Base(DeclarativeBase):
    pass


# Описание сущности в таблице БД
class StudentORM(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    grade: Mapped[int]
    level: Mapped[StudentLevelEnum] = mapped_column(default=StudentLevelEnum.beginner)
    parent_contact: Mapped[str | None]
