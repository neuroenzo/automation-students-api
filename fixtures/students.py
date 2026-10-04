from typing import Any

import pytest
from faker import Faker
from jsonschema import validate

from src.http_client import HTTPClient
from src.models.students import StudentPayload
from src.schemas.students import STUDENT_RESPONSE
from src.students_api import StudentsAPI


@pytest.fixture
def students_api(http_client: HTTPClient) -> StudentsAPI:
    return StudentsAPI(http_client)


@pytest.fixture
def students_cleanup(students_api: StudentsAPI):
    student_ids: set[int] = set()

    yield student_ids

    for student_id in student_ids:
        students_api.delete_student(student_id)


@pytest.fixture
def fake() -> Faker:
    return Faker(locale="ru_Ru")


def _build_student(fake: Faker) -> StudentPayload:
    return StudentPayload(
        email=fake.unique.email(domain="example.com"),
        gender="male",
        name=fake.unique.name(),
        phone_no=fake.unique.numerify(text="+7##########"),
        status=1,
    )


@pytest.fixture
def prepare_student_data(fake: Faker) -> StudentPayload:
    return _build_student(fake)


@pytest.fixture
def created_student(
    students_api: StudentsAPI,
    fake: Faker,
    students_cleanup: set[int],
) -> dict[str, Any]:
    response = students_api.create_student(_build_student(fake))
    data = response.json()

    if "student" in data:
        students_cleanup.add(data["student"]["id"])

    assert response.is_success
    validate(
        instance=data,
        schema=STUDENT_RESPONSE,
    )

    return data["student"]
