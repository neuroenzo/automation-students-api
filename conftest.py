import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from helpers.allure_report import attach_http_history
from src.http_client import HTTPClient

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

pytest_plugins = [
    'fixtures.students',
]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    test_finished = report.when == "call"
    setup_interrupted = report.when == "setup" and not report.passed

    if test_finished or setup_interrupted:
        funcargs = getattr(item, "funcargs", {})
        client = funcargs.get("http_client")
        history = client.history if client is not None else []

        attach_http_history(history)

@pytest.fixture(scope="session")
def base_url() -> str:
    """Возвращает базовый URL тестируемого API из переменных окружения"""
    url = os.getenv("BASE_URL")
    if not url:
        raise RuntimeError("BASE_URL is not set")
    return url.rstrip("/")

@pytest.fixture
def http_client(
    base_url: str,
):
    """Создаёт HTTP-клиент для теста и закрывает его после выполнения"""
    client = HTTPClient(base_url=base_url)
    try:
        yield client
    finally:
        client.close()
