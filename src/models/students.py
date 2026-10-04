from dataclasses import dataclass


@dataclass
class StudentPayload:
    """Данные студента для запросов создания и изменения"""

    email: str
    gender: str
    name: str
    phone_no: str
    status: int
