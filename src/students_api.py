from dataclasses import asdict

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

    def create_student(self, student: StudentPayload) -> httpx.Response:
        return self._http_client.request(
            "POST",
            self.STUDENTS_PATH,
            json=asdict(student),
        )
