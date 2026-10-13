from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app.repository.student import StudentRepository
from app.schemas.student import (  # noqa: F401
    StudentCreateSchema,
    StudentSchema,
    StudentUpdateSchema,
)


class StudentService:
    def __init__(
        self, repo: StudentRepository = Depends(StudentRepository)
    ) -> None:
        self.repo = repo

    async def list_students(self) -> list[StudentSchema]:
        students = await self.repo.list()
        return [StudentSchema.model_validate(s) for s in students]

    async def create_student(
        self, student_create: StudentCreateSchema
    ) -> StudentSchema:
        student = await self.repo.create(student_create)
        return StudentSchema.model_validate(student)

    async def get_student(self, student_id: int) -> StudentSchema:
        student = await self.repo.get_by_id(student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Студент {student_id} не найден",
            )
        return StudentSchema.model_validate(student)

    async def update_student(
        self, student_id: int, student_update: StudentUpdateSchema
    ) -> StudentSchema:
        student = await self.repo.get_by_id(student_id)
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

        student = await self.repo.update(student, updated_data)
        return StudentSchema.model_validate(student)

    async def delete_student(self, student_id: int) -> None:
        student = await self.repo.get_by_id(student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Студент {student_id} не найден",
            )

        # нельзя удалить студента у которого есть уроки — в них деньги
        if await self.repo.has_lessons(student_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"У студента {student_id} есть уроки",
            )

        await self.repo.delete(student)
