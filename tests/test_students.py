from dataclasses import asdict
from typing import Any

import allure
import pytest
from jsonschema import validate

from src.models.students import StudentPayload
from src.schemas.students import DELETE_STUDENT_RESPONSE, STUDENT_RESPONSE, STUDENTS
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
        prepare_student_data: StudentPayload,
        students_cleanup: set[int],
    ) -> None:
        with allure.step("Отправить POST /student"):
            response = students_api.create_student(prepare_student_data)
            data = response.json()
            students_cleanup.add(data["student"]["id"])

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 201

        with allure.step("Проверить тело ответа"):
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
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "missing_field",
        [
            "email",
            "gender",
            "name",
            "phone_no",
            "status",
        ],
    )
    @allure.title("Создание студента без обязательного поля: {missing_field}")
    def test_create_student_without_required_field(
        self,
        students_api: StudentsAPI,
        prepare_student_data: StudentPayload,
        students_cleanup: set[int],
        missing_field: str,
    ) -> None:
        student_payload = asdict(prepare_student_data)
        student_payload.pop(missing_field)

        with allure.step(f"Отправить POST /student без поля {missing_field}"):
            response = students_api.create_student(student_payload)
            data = response.json()

            if "student" in data:
                students_cleanup.add(data["student"]["id"])

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 400

        with allure.step("Проверить тело ответа"):
            assert data == {
                "message": "Wrong JSON, student not created",
                "status": 0,
            }

    @pytest.mark.api
    @pytest.mark.negative
    @allure.title("Повторное создание студента с одинаковыми данными")
    def test_create_duplicate_student(
        self,
        students_api: StudentsAPI,
        prepare_student_data: StudentPayload,
        students_cleanup: set[int],
    ) -> None:
        with allure.step("Создать студента"):
            first_response = students_api.create_student(prepare_student_data)
            first_data = first_response.json()
            students_cleanup.add(first_data["student"]["id"])

            assert first_response.is_success
            validate(
                instance=first_data,
                schema=STUDENT_RESPONSE,
            )
            assert first_data["status"] == 1

        with allure.step("Повторно создать студента с теми же данными"):
            second_response = students_api.create_student(prepare_student_data)
            second_data = second_response.json()

            if "student" in second_data:
                students_cleanup.add(second_data["student"]["id"])

        with allure.step("Проверить статус повторного создания"):
            assert second_response.status_code == 409

        with allure.step("Проверить тело ответа"):
            assert isinstance(second_data["message"], str)

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

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    @allure.title("Удаление студента")
    def test_delete_student(
        self,
        students_api: StudentsAPI,
        created_student: dict[str, Any],
        students_cleanup: set[int],
    ) -> None:
        student_id = created_student["id"]

        with allure.step(f"Отправить DELETE /student/{student_id}"):
            response = students_api.delete_student(student_id)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа"):
            data = response.json()

            validate(
                instance=data,
                schema=DELETE_STUDENT_RESPONSE,
            )

            assert data["message"] == "Student deleted successfully"
            assert data["status"] == 1
            students_cleanup.discard(student_id)

        with allure.step("Проверить отсутствие студента в списке"):
            students_response = students_api.get_students()
            assert students_response.status_code == 200

            students_data = students_response.json()
            validate(
                instance=students_data,
                schema=STUDENTS,
            )

            assert created_student not in students_data["students"]

    @pytest.mark.api
    @pytest.mark.negative
    @allure.title("Повторное удаление студента")
    def test_delete_student_twice(
        self,
        students_api: StudentsAPI,
        created_student: dict[str, Any],
        students_cleanup: set[int],
    ) -> None:
        student_id = created_student["id"]

        with allure.step(f"Удалить студента DELETE /student/{student_id}"):
            first_response = students_api.delete_student(student_id)
            assert first_response.status_code == 200
            students_cleanup.discard(student_id)

        with allure.step(f"Повторно удалить студента DELETE /student/{student_id}"):
            second_response = students_api.delete_student(student_id)

        with allure.step("Проверить статус повторного удаления"):
            assert second_response.status_code == 404

        with allure.step("Проверить тело ответа"):
            data = second_response.json()

            validate(
                instance=data,
                schema=DELETE_STUDENT_RESPONSE,
            )
