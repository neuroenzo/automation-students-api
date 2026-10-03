import allure
import pytest
from jsonschema import validate

from src.students_api import StudentsAPI
from src.schemas.students import STUDENTS


@allure.feature("Students API")
class TestStudents:
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.title("Получение списка студентов")
    def test_get_students(self, students_api: StudentsAPI) -> None:
        """Тест успешного получения списка студентов"""
        with allure.step("Отправить GET /student"):
            response = students_api.get_students()

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа"):
            data = response.json()

            validate(
                instance=data,
                schema=STUDENTS,
            )

            assert data["status"] == 1
            assert isinstance(data["students"], list)
