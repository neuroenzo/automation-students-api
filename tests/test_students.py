import pytest
from jsonschema import validate

from src.students_api import StudentsAPI
from src.schemas.students import STUDENTS


class TestStudents:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_students(self, students_api: StudentsAPI) -> None:
        """Тест успешного получения списка студентов."""
        response = students_api.get_students()

        assert response.status_code == 200

        data = response.json()

        validate(
            instance=data,
            schema=STUDENTS,
        )

        assert data["status"] == 1
        assert isinstance(data["students"], list)
