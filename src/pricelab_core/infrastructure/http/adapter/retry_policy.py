import asyncio
import functools
from typing import ParamSpec, TypeVar, Callable, Awaitable, Optional

from pricelab_core.infrastructure.http.configuration.retry_configuration import RetrySettings

P = ParamSpec("P")
R = TypeVar("R")


class RetryPolicy:
    def __init__(self, settings: Optional[RetrySettings] = None):
        self._settings = settings or RetrySettings()

    @property
    def settings(self) -> RetrySettings:
        return self._settings

    def decorator(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:

            last_exception = None
            retries = self._settings.retries + 1
            base_delay = self._settings.base_delay
            retry_on = self._settings.retry_on

            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)

                except retry_on as exception:
                    last_exception = exception

                    if attempt == retries - 1:
                        raise

                    delay = base_delay * (2**attempt)

                    await asyncio.sleep(delay)

            raise last_exception or RuntimeError("RetryPolicy failed without exception")

        return wrapper
