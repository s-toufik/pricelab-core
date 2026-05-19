import asyncio
import functools
from typing import Type, Tuple, ParamSpec, TypeVar, Callable, Awaitable

from pricelab_core.infrastructure.http.configuration.retry_configuration import RetrySettings

P = ParamSpec("P")
R = TypeVar("R")


class RetryPolicy:
    def __init__(self, settings: RetrySettings = RetrySettings()):
        self._settings = settings
        self._retries: int = settings.retries
        self._base_delay: float = settings.base_delay
        self._retry_on: Tuple[Type[Exception], ...] = settings.retry_on

    @property
    def settings(self) -> RetrySettings:
        return self._settings

    def decorator(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:

            last_exception = None

            for attempt in range(self._retries):
                try:
                    return await func(*args, **kwargs)

                except self._retry_on as exception:
                    last_exception = exception

                    if attempt == self._retries - 1:
                        raise

                    delay = self._base_delay * (2**attempt)

                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper
