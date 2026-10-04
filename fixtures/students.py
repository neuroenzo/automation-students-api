import pytest
from faker import Faker

from src.http_client import HTTPClient
from src.models.students import StudentPayload
from src.students_api import StudentsAPI


@pytest.fixture
def students_api(http_client: HTTPClient) -> StudentsAPI:
    """Предоставляет API-клиент для выполнения операций со студентами"""
    return StudentsAPI(http_client)


@pytest.fixture
def new_student() -> StudentPayload:
    """Подготавливает уникальные тестовые данные для создания нового студента"""
    fake = Faker(locale="en_US")

    return StudentPayload(
        email=fake.unique.email(domain="example.com"),
        gender="male",
        name=fake.unique.name(),
        phone_no=fake.unique.numerify(text="+7##########"),
        status=1,
    )
