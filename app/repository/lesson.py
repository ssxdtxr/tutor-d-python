from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonStatusEnum


class LessonRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_by_id(self, lesson_id: int) -> Lesson | None:
        return await self.session.get(Lesson, lesson_id)

    async def list(
        self,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        student_id: int | None = None,
        lesson_status: LessonStatusEnum | None = None,
    ) -> list[Lesson]:
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

        # сортировка по возрастанию времени начала, второй ключ — id для стабильности
        query = query.order_by(Lesson.starts_at, Lesson.id)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(
        self,
        data: LessonCreate,
        starts_at: datetime,
        ends_at: datetime,
    ) -> Lesson:
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
        return lesson

    async def update(self, lesson: Lesson, data: dict) -> Lesson:
        for field, value in data.items():
            setattr(lesson, field, value)
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson

    async def delete(self, lesson: Lesson) -> None:
        await self.session.delete(lesson)
        await self.session.commit()

    async def find_overlap(
        self,
        starts_at: datetime,
        ends_at: datetime,
        exclude_id: int | None = None,
    ) -> Lesson | None:
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
        return result.scalars().first()
