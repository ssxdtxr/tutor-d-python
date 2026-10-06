from fastapi import APIRouter, Depends, status

from app.schemas.student import StudentCreateSchema, StudentSchema, StudentUpdateSchema
from app.services.student import StudentService

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/")
def list_students(
    student_service: StudentService = Depends(StudentService),
) -> list[StudentSchema]:
    return student_service.list_students()

@router.get("/{student_id}")
def get_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
):
    return student_service.get_student(student_id=student_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreateSchema,
    student_service: StudentService = Depends(StudentService),
) -> StudentSchema:
    return student_service.create_student(student_create=payload)


@router.patch("/{student_id}")
def update_student(
    payload: StudentUpdateSchema,
    student_id: int,
    student_service: StudentService = Depends(StudentService),
) -> StudentSchema:
    return student_service.update_student(student_id=student_id, student_update=payload)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
) -> None:
    return student_service.delete_student(student_id=student_id)
