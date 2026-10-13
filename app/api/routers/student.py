from fastapi import APIRouter, Depends, status

from app.schemas.student import StudentCreateSchema, StudentSchema, StudentUpdateSchema
from app.services.student import StudentService

router = APIRouter(prefix="/students", tags=["students"])


# "" вместо "/" — без редиректа 307 при запросе без слэша
@router.get(
    "",
    summary="Список всех учеников",
    responses={200: {"description": "Успешно"}},
)
async def list_students(
    # Depends(StudentService) — FastAPI создаёт сервис с сессией из get_session
    student_service: StudentService = Depends(StudentService),
) -> list[StudentSchema]:
    return await student_service.list_students()


@router.get(
    "/{student_id}",
    summary="Получить ученика по ID",
    responses={
        200: {"description": "Успешно"},
        404: {"description": "Ученик не найден"},
    },
)
async def get_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
) -> StudentSchema:
    return await student_service.get_student(student_id=student_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Создать ученика",
    responses={
        201: {"description": "Ученик создан"},
        422: {"description": "Ошибка валидации"},
    },
)
async def create_student(
    payload: StudentCreateSchema,
    student_service: StudentService = Depends(StudentService),
) -> StudentSchema:
    return await student_service.create_student(student_create=payload)


@router.patch(
    "/{student_id}",
    summary="Обновить данные ученика",
    responses={
        200: {"description": "Успешно обновлено"},
        404: {"description": "Ученик не найден"},
        422: {"description": "Ошибка валидации"},
    },
)
async def update_student(
    payload: StudentUpdateSchema,
    student_id: int,
    student_service: StudentService = Depends(StudentService),
) -> StudentSchema:
    return await student_service.update_student(
        student_id=student_id, student_update=payload
    )


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить ученика",
    responses={
        204: {"description": "Успешно удалено"},
        404: {"description": "Ученик не найден"},
    },
)
async def delete_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
) -> None:
    return await student_service.delete_student(student_id=student_id)
