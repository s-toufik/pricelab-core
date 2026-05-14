from typing import Protocol, Any, Optional


class HttpClient(Protocol):
    async def start(self) -> None: ...
    async def close(self) -> None: ...
    async def get(
        self,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any: ...
    async def post(
        self,
        endpoint: str,
        *,
        body: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any: ...
