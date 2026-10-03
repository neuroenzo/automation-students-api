from dataclasses import dataclass
from typing import Any

import httpx


@dataclass
class HTTPExchange:
    """Данные одного HTTP-вызова: запрос, ответ или ошибка."""

    request: httpx.Request
    response: httpx.Response | None = None
    error_type: str | None = None
    error_message: str | None = None


class HTTPClient:
    """Настриаваемая обертка для HTTP-запросов к тестируемому API."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            follow_redirects=False,
        )
        self.history: list[HTTPExchange] = []

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        try:
            response = self._client.request(
                method=method,
                url=path,
                **kwargs,
            )
        except httpx.RequestError as error:
            self.history.append(
                HTTPExchange(
                    request=error.request,
                    error_type=type(error).__name__,
                    error_message=str(error),
                )
            )
            raise

        self.history.append(
            HTTPExchange(
                request=response.request,
                response=response,
            )
        )
        return response

    def close(self) -> None:
        """Закрывает сетевые соединения и освобождает связанные ресурсы."""
        self._client.close()
