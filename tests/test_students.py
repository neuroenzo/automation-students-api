from dataclasses import asdict

import allure
import pytest
from jsonschema import validate

from src.models.students import StudentPayload
from src.schemas.students import CREATE_STUDENT_RESPONSE, STUDENTS
from src.students_api import StudentsAPI


@allure.feature("Students API")
class TestStudents:
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    @allure.title("Получение списка студентов")
    def test_get_students(self, students_api: StudentsAPI) -> None:
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

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    @allure.title("Создание студента")
    def test_create_student(
        self,
        students_api: StudentsAPI,
        new_student: StudentPayload,
    ) -> None:
        with allure.step("Отправить POST /student"):
            response = students_api.create_student(new_student)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа"):
            data = response.json()

            validate(
                instance=data,
                schema=CREATE_STUDENT_RESPONSE,
            )

            assert data["message"] == "Student created successfully"
            assert data["status"] == 1
            assert data["student"]["id"] > 0
            assert {
                field: value
                for field, value in data["student"].items()
                if field != "id"
            } == asdict(new_student)

        with allure.step("Проверить, что студент появился в списке"):
            students_response = students_api.get_students()
            assert students_response.status_code == 200

            students_data = students_response.json()
            validate(
                instance=students_data,
                schema=STUDENTS,
            )

            assert data["student"] in students_data["students"]
