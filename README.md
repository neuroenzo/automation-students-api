## Автоматизированные тесты Students API

### Технологии

- Python 3.14
- pytest
- HTTPX
- JSON Schema
- Faker
- Allure
- Ruff
- uv

### Структура проекта

```text
automation-students-api/
├── fixtures/              # Pytest-fixtures и подготовка тестовых данных
├── helpers/               # Формирование вложений для Allure
├── src/
│   ├── models/            # Модели данных запросов
│   ├── schemas/           # JSON-схемы ответов API
│   ├── http_client.py     # HTTP-клиент и история запросов
│   └── students_api.py    # Методы Students API
├── tests/                 # API-тесты
├── conftest.py            # Общие fixtures и pytest hooks
├── pyproject.toml         # Зависимости и настройки pytest
└── uv.lock                # Зафиксированные версии зависимостей
```

### Быстрый старт

#### Установка

Для работы нужен установленный `uv`.

```shell
uv sync
cp .env.example .env
```

Укажите адрес тестируемого API в созданном файле `.env`.

#### Запуск

```shell
uv run pytest -v -s -l
```

#### Allure-отчет

Запуск тестов с формированием результатов Allure:

```shell
uv run pytest -v -s -l --alluredir=allure-results
```

Результаты Allure сохраняются в `allure-results`.

Для просмотра отчета нужен установленный Allure CLI:

```shell
allure serve allure-results
```
