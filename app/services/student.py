from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.student import Student
from app.schemas.student import StudentCreateSchema, StudentSchema, StudentUpdateSchema


class StudentService:
    # сессия создаётся FastAPI через Depends и живёт один HTTP-запрос
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def list_students(self) -> list[StudentSchema]:
        # select(Student) → SELECT * FROM students
        result = await self.session.execute(select(Student))
        # scalars() убирает обёртку Row, all() возвращает список ORM-объектов
        students = result.scalars().all()
        return [StudentSchema.model_validate(s) for s in students]

    async def create_student(
        self, student_create: StudentCreateSchema
    ) -> StudentSchema:
        # **model_dump() разворачивает схему в kwargs для ORM-модели
        student = Student(**student_create.model_dump())
        self.session.add(student)
        await self.session.commit()
        # refresh подтягивает id и created_at, которые проставила база
        await self.session.refresh(student)
        return StudentSchema.model_validate(student)

    async def get_student(self, student_id: int) -> StudentSchema:
        # session.get — поиск по первичному ключу, быстрее чем select + where
        student = await self.session.get(Student, student_id)

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Студент {student_id} не найден",
            )

        return StudentSchema.model_validate(student)

    async def update_student(
        self, student_id: int, student_update: StudentUpdateSchema
    ) -> StudentSchema:
        student = await self.session.get(Student, student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Студент {student_id} не найден",
            )

        # exclude_unset=True — берём только поля, которые пришли в запросе
        updated_data = student_update.model_dump(exclude_unset=True)

        # валидируем итоговое состояние до записи в БД
        try:
            current = StudentSchema.model_validate(student)
            StudentSchema.model_validate(
                current.model_copy(update=updated_data).model_dump()
            )
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=e.errors(),
            ) from e

        # применяем изменения к ORM-объекту
        for field, value in updated_data.items():
            setattr(student, field, value)

        await self.session.commit()
        await self.session.refresh(student)
        return StudentSchema.model_validate(student)

    async def delete_student(self, student_id: int) -> None:
        student = await self.session.get(Student, student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Студент {student_id} не найден",
            )
        await self.session.delete(student)
        await self.session.commit()
