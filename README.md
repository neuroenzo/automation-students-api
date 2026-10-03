## Автоматизированные тесты для Students API.

### Установка

uv sync
cp .env.example .env

### Запуск

```shell
uv run pytest -v -s -l
```

Результаты Allure сохраняются в `allure-results`.

### Allure-отчёт

Для просмотра отчёта нужен установленный Allure CLI:

```shell
allure serve allure-results
```
