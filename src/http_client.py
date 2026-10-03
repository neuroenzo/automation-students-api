from typing import Any

import httpx


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

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        return self._client.request(
            method=method,
            url=path,
            **kwargs,
        )

    def close(self) -> None:
        """Закрывает сетевые соединения и освобождает связанные ресурсы."""
        self._client.close()
