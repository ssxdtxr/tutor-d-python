from itertools import count

from fastapi import HTTPException, status

from app.schemas.student import StudentCreateSchema, StudentSchema, StudentUpdateSchema

students: list[StudentSchema] = list()

_id_counter = count(1)

class StudentService:
    def list_students(self) -> list[StudentSchema]:
        return students

    def create_student(self, student_create: StudentCreateSchema) -> StudentSchema:
        new_student = StudentSchema(
            id=str(next(_id_counter)),
            name=student_create.name,
            age=student_create.age,
            grade=student_create.grade,
            level=student_create.level,
            parent_contact=student_create.parent_contact,
        )

        students.append(new_student)

        return new_student

    def get_student(self, student_id: str) -> StudentSchema:
        for student in students:
            if student.id == student_id:
                return student

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент {student_id} не найден",
        )

    def update_student(
        self, student_id: str, student_update: StudentUpdateSchema
    ) -> StudentSchema:

        for i, student in enumerate(students):
            if student.id == student_id:
                updated_data = student_update.model_dump(exclude_unset=True)
                updated_student = student.model_copy(update=updated_data)
                StudentSchema.model_validate(updated_student.model_dump())

                students[i] = updated_student

                return updated_student

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент {student_id} не найден",
        )

    def delete_student(self, student_id: str) -> None:
        for i, student in enumerate(students):
            if student.id == student_id:
                students.pop(i)
                return None

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Студент {student_id} не найден",
        )
