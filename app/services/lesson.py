from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status

from app.repository.lesson import LessonRepository
from app.repository.student import StudentRepository
from app.schemas.lesson import LessonCreate, LessonRead, LessonStatusEnum, LessonUpdate


class LessonService:
    def __init__(
        self,
        lesson_repo: LessonRepository = Depends(LessonRepository),
        student_repo: StudentRepository = Depends(StudentRepository),
    ) -> None:
        self.lesson_repo = lesson_repo
        self.student_repo = student_repo

    async def list_lessons(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        student_id: int | None = None,
        lesson_status: LessonStatusEnum | None = None,
    ) -> list[LessonRead]:
        lessons = await self.lesson_repo.list(
            date_from=date_from,
            date_to=date_to,
            student_id=student_id,
            lesson_status=lesson_status,
        )
        return [LessonRead.model_validate(lesson) for lesson in lessons]

    async def create_lesson(self, data: LessonCreate) -> LessonRead:
        # переводим в UTC для единообразного хранения
        starts_at = data.starts_at.astimezone(UTC)

        # нельзя создать урок в прошлом
        if starts_at < datetime.now(UTC):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Урок не может быть в прошлом",
            )

        ends_at = starts_at + timedelta(minutes=data.duration_min)

        # проверяем что ученик существует
        student = await self.student_repo.get_by_id(data.student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Ученик {data.student_id} не найден",
            )

        # проверяем пересечения с неотменёнными уроками
        await self._check_overlap(starts_at, ends_at)

        lesson = await self.lesson_repo.create(data, starts_at, ends_at)
        return LessonRead.model_validate(lesson)

    async def get_lesson(self, lesson_id: int) -> LessonRead:
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if lesson is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Урок {lesson_id} не найден",
            )
        return LessonRead.model_validate(lesson)

    async def update_lesson(self, lesson_id: int, data: LessonUpdate) -> LessonRead:
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if lesson is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Урок {lesson_id} не найден",
            )

        updated = data.model_dump(exclude_unset=True)

        # пересчитываем ends_at если меняется время или длительность
        new_starts_at = lesson.starts_at
        new_duration = lesson.duration_min

        if "starts_at" in updated:
            new_starts_at = updated["starts_at"].astimezone(UTC)
            updated["starts_at"] = new_starts_at
            # нельзя перенести урок в прошлое
            if new_starts_at < datetime.now(UTC):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Урок не может быть в прошлом",
                )

        if "duration_min" in updated:
            new_duration = updated["duration_min"]

        new_ends_at = new_starts_at + timedelta(minutes=new_duration)

        # проверяем пересечения, исключая сам урок
        await self._check_overlap(new_starts_at, new_ends_at, exclude_id=lesson_id)

        updated["ends_at"] = new_ends_at
        lesson = await self.lesson_repo.update(lesson, updated)
        return LessonRead.model_validate(lesson)

    async def delete_lesson(self, lesson_id: int) -> None:
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if lesson is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Урок {lesson_id} не найден",
            )
        await self.lesson_repo.delete(lesson)

    async def _check_overlap(
        self,
        starts_at: datetime,
        ends_at: datetime,
        exclude_id: int | None = None,
    ) -> None:
        conflict = await self.lesson_repo.find_overlap(starts_at, ends_at, exclude_id)
        if conflict is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Урок пересекается с уроком {conflict.id}",
            )
