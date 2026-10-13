from datetime import datetime

from fastapi import APIRouter, Depends, status

from app.schemas.lesson import LessonCreate, LessonRead, LessonStatusEnum, LessonUpdate
from app.services.lesson import LessonService

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get(
    "",
    summary="Список уроков",
    responses={200: {"description": "Успешно"}},
)
async def list_lessons(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    student_id: int | None = None,
    lesson_status: LessonStatusEnum | None = None,
    lesson_service: LessonService = Depends(LessonService),
) -> list[LessonRead]:
    return await lesson_service.list_lessons(
        date_from=date_from,
        date_to=date_to,
        student_id=student_id,
        lesson_status=lesson_status,
    )


@router.get(
    "/{lesson_id}",
    summary="Получить урок по ID",
    responses={
        200: {"description": "Успешно"},
        404: {"description": "Урок не найден"},
    },
)
async def get_lesson(
    lesson_id: int,
    lesson_service: LessonService = Depends(LessonService),
) -> LessonRead:
    return await lesson_service.get_lesson(lesson_id=lesson_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Создать урок",
    responses={
        201: {"description": "Урок создан"},
        409: {"description": "Пересечение с другим уроком"},
        422: {"description": "Ошибка валидации"},
    },
)
async def create_lesson(
    payload: LessonCreate,
    lesson_service: LessonService = Depends(LessonService),
) -> LessonRead:
    return await lesson_service.create_lesson(data=payload)


@router.patch(
    "/{lesson_id}",
    summary="Обновить урок",
    responses={
        200: {"description": "Успешно обновлено"},
        404: {"description": "Урок не найден"},
        409: {"description": "Пересечение с другим уроком"},
        422: {"description": "Ошибка валидации"},
    },
)
async def update_lesson(
    lesson_id: int,
    payload: LessonUpdate,
    lesson_service: LessonService = Depends(LessonService),
) -> LessonRead:
    return await lesson_service.update_lesson(lesson_id=lesson_id, data=payload)


@router.delete(
    "/{lesson_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить урок",
    responses={
        204: {"description": "Успешно удалено"},
        404: {"description": "Урок не найден"},
    },
)
async def delete_lesson(
    lesson_id: int,
    lesson_service: LessonService = Depends(LessonService),
) -> None:
    return await lesson_service.delete_lesson(lesson_id=lesson_id)
