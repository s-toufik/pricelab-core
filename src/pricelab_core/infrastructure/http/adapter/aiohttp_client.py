import aiohttp
import orjson

from typing import Any, Optional

from pricelab_core.infrastructure.http.enum.http_method import HttpMethod


class AioHttpClient:
    DEFAULT_TIMEOUT = 30
    KEEPALIVE_TIMEOUT = 60
    CONNECTOR_LIMIT = 1000
    CONNECTOR_LIMIT_PER_HOST = 100
    CONNECTOR_ENABLE_CLEANUP_CLOSED = True
    CONNECTOR_TTL_DNS_CACHE = 600

    SSL = None

    def __init__(self, base_url: str, timeout: int | None = None) -> None:
        self._base_url = base_url.rstrip("/") + "/"
        self._timeout = aiohttp.ClientTimeout(total=timeout or self.DEFAULT_TIMEOUT)
        self._connector = aiohttp.TCPConnector(
            limit=self.CONNECTOR_LIMIT,
            limit_per_host=self.CONNECTOR_LIMIT_PER_HOST,
            enable_cleanup_closed=self.CONNECTOR_ENABLE_CLEANUP_CLOSED,
            ttl_dns_cache=self.CONNECTOR_TTL_DNS_CACHE,
            ssl=self.SSL,
            keepalive_timeout=self.KEEPALIVE_TIMEOUT,
        )
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AioHttpClient":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def start(self) -> None:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=self._timeout,
                connector=self._connector,
            )

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        await self._connector.close()
        self._session = None

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:

        session = self._ensure_session()

        async with session.request(
            method=method, url=self._build_url(endpoint), params=params, json=json, headers=headers
        ) as response:
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                return orjson.loads(await response.read())

            return await response.text()

    async def get(
        self,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:

        return await self.request(HttpMethod.GET.value, endpoint, params=params, headers=headers)

    async def post(
        self,
        endpoint: str,
        *,
        body: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:

        return await self.request(HttpMethod.POST.value, endpoint, json=body, headers=headers)

    def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            raise RuntimeError("Client session is not started. Call start() first.")

        return self._session

    def _build_url(self, endpoint: str) -> str:
        return self._base_url + endpoint.lstrip("/")
