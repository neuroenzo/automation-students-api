import httpx

from src.http_client import HTTPClient


class StudentsAPI:
    """Методы для работы с эндпоинтами студентов."""

    STUDENTS_PATH = "/student"

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_students(self) -> httpx.Response:
        """Возвращает спискок студентов."""
        return self._http_client.request(
            "GET",
            self.STUDENTS_PATH,
        )
