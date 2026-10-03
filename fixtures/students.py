import pytest

from src.students_api import StudentsAPI
from src.http_client import HTTPClient


@pytest.fixture
def students_api(http_client: HTTPClient) -> StudentsAPI:
    """Предоставляет API-клиент для выполнения операций со студентами."""
    return StudentsAPI(http_client)
