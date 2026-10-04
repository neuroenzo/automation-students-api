import json
from typing import Any

import allure
import httpx

from src.http_client import HTTPExchange

SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
}


def _mask_headers(headers: httpx.Headers) -> dict[str, str]:
    """Скрывает чувствительные значения HTTP-заголовков"""
    return {
        name: "***" if name.lower() in SENSITIVE_HEADERS else value
        for name, value in headers.items()
    }


def _parse_body(content: bytes) -> Any:
    """Преобразует тело запроса или ответа в JSON либо текст"""
    if not content:
        return None

    text = content.decode("utf-8", errors="replace")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def attach_http_history(history: list[HTTPExchange]) -> None:
    """Прикладывает лог HTTP-вызовов к текущему тесту в Allure"""
    exchanges = []

    for index, exchange in enumerate(history, start=1):
        response = exchange.response

        exchanges.append({
            "number": index,
            "request": {
                "method": exchange.request.method,
                "url": str(exchange.request.url),
                "headers": _mask_headers(exchange.request.headers),
                "body": _parse_body(exchange.request.content),
            },
            "response": (
                {
                    "status_code": response.status_code,
                    "headers": _mask_headers(response.headers),
                    "body": _parse_body(response.content),
                }
                if response is not None
                else None
            ),
            "error": (
                {
                    "type": exchange.error_type,
                    "message": exchange.error_message,
                }
                if exchange.error_type is not None
                else None
            ),
        })

    log = {
        "request_count": len(exchanges),
        "exchanges": exchanges,
    }

    allure.attach(
        json.dumps(log, ensure_ascii=False, indent=2),
        name="HTTP log",
        attachment_type=allure.attachment_type.JSON,
    )
