from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.lesson import Lesson
from app.models.student import Student
from app.schemas.student import StudentCreateSchema


class StudentRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_by_id(self, student_id: int) -> Student | None:
        # session.get — поиск по первичному ключу, быстрее чем select + where
        return await self.session.get(Student, student_id)

    async def list(self) -> list[Student]:
        result = await self.session.execute(select(Student))
        return list(result.scalars().all())

    async def create(self, data: StudentCreateSchema) -> Student:
        # **model_dump() разворачивает схему в kwargs для ORM-модели
        student = Student(**data.model_dump())
        self.session.add(student)
        await self.session.commit()
        # refresh подтягивает id и created_at, которые проставила база
        await self.session.refresh(student)
        return student

    async def update(self, student: Student, data: dict) -> Student:
        for field, value in data.items():
            setattr(student, field, value)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def delete(self, student: Student) -> None:
        await self.session.delete(student)
        await self.session.commit()

    async def has_lessons(self, student_id: int) -> bool:
        # проверяем есть ли хоть один урок у студента
        result = await self.session.execute(
            select(Lesson).where(Lesson.student_id == student_id).limit(1)
        )
        return result.scalars().first() is not None
