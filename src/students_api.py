from dataclasses import asdict
from typing import Any

import httpx

from src.http_client import HTTPClient
from src.models.students import StudentPayload


class StudentsAPI:
    """Методы для работы с эндпоинтами студентов"""

    STUDENTS_PATH = "/student"

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_students(self) -> httpx.Response:
        return self._http_client.request(
            "GET",
            self.STUDENTS_PATH,
        )

    def create_student(
        self,
        student: StudentPayload | dict[str, Any],
    ) -> httpx.Response:
        payload = asdict(student) if isinstance(student, StudentPayload) else student

        return self._http_client.request(
            "POST",
            self.STUDENTS_PATH,
            json=payload,
        )

    def update_student(
        self,
        student_id: int,
        student: StudentPayload,
    ) -> httpx.Response:
        return self._http_client.request(
            "PUT",
            f"{self.STUDENTS_PATH}/{student_id}",
            json=asdict(student),
        )

    def delete_student(self, student_id: int) -> httpx.Response:
        return self._http_client.request(
            "DELETE",
            f"{self.STUDENTS_PATH}/{student_id}",
        )
