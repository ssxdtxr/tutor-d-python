from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.lesson import Lesson
from app.models.student import Student
from app.schemas.lesson import LessonCreate, LessonRead, LessonStatusEnum, LessonUpdate


class LessonService:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def list_lessons(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        student_id: int | None = None,
        lesson_status: LessonStatusEnum | None = None,
    ) -> list[LessonRead]:
        query = select(Lesson)

        # фильтр по началу урока: date_from <= starts_at < date_to
        if date_from is not None:
            query = query.where(Lesson.starts_at >= date_from)
        if date_to is not None:
            query = query.where(Lesson.starts_at < date_to)
        if student_id is not None:
            query = query.where(Lesson.student_id == student_id)
        if lesson_status is not None:
            query = query.where(Lesson.status == lesson_status)

        # сортировка по возрастанию времени начала
        query = query.order_by(Lesson.starts_at)

        result = await self.session.execute(query)
        lessons = result.scalars().all()
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
        student = await self.session.get(Student, data.student_id)
        if student is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Ученик {data.student_id} не найден",
            )

        # проверяем пересечения с неотменёнными уроками
        await self._check_overlap(starts_at, ends_at)

        lesson = Lesson(
            student_id=data.student_id,
            starts_at=starts_at,
            ends_at=ends_at,
            duration_min=data.duration_min,
            topic=data.topic,
            status=LessonStatusEnum.planned,
            price=data.price,
        )
        self.session.add(lesson)
        await self.session.commit()
        await self.session.refresh(lesson)
        return LessonRead.model_validate(lesson)

    async def get_lesson(self, lesson_id: int) -> LessonRead:
        lesson = await self.session.get(Lesson, lesson_id)
        if lesson is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Урок {lesson_id} не найден",
            )
        return LessonRead.model_validate(lesson)

    async def update_lesson(self, lesson_id: int, data: LessonUpdate) -> LessonRead:
        lesson = await self.session.get(Lesson, lesson_id)
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
        for field, value in updated.items():
            setattr(lesson, field, value)

        await self.session.commit()
        await self.session.refresh(lesson)
        return LessonRead.model_validate(lesson)

    async def delete_lesson(self, lesson_id: int) -> None:
        lesson = await self.session.get(Lesson, lesson_id)
        if lesson is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Урок {lesson_id} не найден",
            )
        await self.session.delete(lesson)
        await self.session.commit()

    async def _check_overlap(
        self,
        starts_at: datetime,
        ends_at: datetime,
        exclude_id: int | None = None,
    ) -> None:
        # пересечение: starts_new < ends_existing AND starts_existing < ends_new
        # впритык (ends_a == starts_b) — не пересечение
        query = select(Lesson).where(
            Lesson.status != LessonStatusEnum.cancelled,
            Lesson.starts_at < ends_at,
            Lesson.ends_at > starts_at,
        )
        if exclude_id is not None:
            query = query.where(Lesson.id != exclude_id)

        result = await self.session.execute(query)
        conflict = result.scalars().first()
        if conflict is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Урок пересекается с уроком {conflict.id}",
            )
