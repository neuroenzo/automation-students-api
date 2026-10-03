import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from src.http_client import HTTPClient

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

pytest_plugins = [
    'fixtures.students',
]

@pytest.fixture(scope="session")
def base_url() -> str:
    """Возвращает базовый URL тестируемого API из переменных окружения."""
    url = os.getenv("BASE_URL")
    if not url:
        raise RuntimeError("BASE_URL is not set")
    return url.rstrip("/")

@pytest.fixture
def http_client(base_url: str):
    """Создаёт HTTP-клиент для теста и закрывает его после выполнения."""
    client = HTTPClient(base_url=base_url)
    yield client
    client.close()
