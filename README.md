## Автоматизированные тесты для Students API

### Установка

Для работы нужен отдельно установленный uv

uv sync
cp .env.example .env

### Запуск

```shell
uv run pytest -v -s -l
```

### Allure-отчет

### Запуск с allure-отчетом
```shell
uv run pytest -v -s -l --alluredir=allure-results
```
Результаты Allure сохраняются в `allure-results`.

Для просмотра отчета нужен установленный Allure CLI:

```shell
allure serve allure-results
```
