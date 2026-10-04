from dataclasses import asdict
from typing import Any

import allure
import pytest
from jsonschema import validate

from src.models.students import StudentPayload
from src.schemas.students import STUDENT_RESPONSE, STUDENTS
from src.students_api import StudentsAPI


@allure.feature("API для управления студентами")
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
        prepare_student_data: StudentPayload,
    ) -> None:
        with allure.step("Отправить POST /student"):
            response = students_api.create_student(prepare_student_data)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа"):
            data = response.json()

            validate(
                instance=data,
                schema=STUDENT_RESPONSE,
            )

            assert data["message"] == "Student created successfully"
            assert data["status"] == 1
            assert data["student"]["id"] > 0
            assert {
                field: value
                for field, value in data["student"].items()
                if field != "id"
            } == asdict(prepare_student_data)

        with allure.step("Проверить, что студент появился в списке"):
            students_response = students_api.get_students()
            assert students_response.status_code == 200

            students_data = students_response.json()
            validate(
                instance=students_data,
                schema=STUDENTS,
            )

            assert data["student"] in students_data["students"]

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    @allure.title("Обновление студента")
    def test_update_student(
        self,
        students_api: StudentsAPI,
        created_student: dict[str, Any],
        prepare_student_data: StudentPayload,
    ) -> None:
        student_id = created_student["id"]

        with allure.step(f"Отправить PUT /student/{student_id}"):
            response = students_api.update_student(
                student_id=student_id,
                student=prepare_student_data,
            )

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа"):
            data = response.json()

            validate(
                instance=data,
                schema=STUDENT_RESPONSE,
            )

            assert data["message"] == "Student updated successfully"
            assert data["status"] == 1
            assert data["student"]["id"] == student_id
            assert {
                field: value
                for field, value in data["student"].items()
                if field != "id"
            } == asdict(prepare_student_data)

        with allure.step("Проверить изменённого студента в списке"):
            students_response = students_api.get_students()
            assert students_response.status_code == 200

            students_data = students_response.json()
            validate(
                instance=students_data,
                schema=STUDENTS,
            )

            assert data["student"] in students_data["students"]
            assert created_student not in students_data["students"]
