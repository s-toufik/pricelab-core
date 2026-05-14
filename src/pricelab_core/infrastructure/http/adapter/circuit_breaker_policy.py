import time
from typing import ParamSpec

from pricelab_core.infrastructure.http.configuration.circuite_breaker_configuration import (
    CircuitBreakerSettings,
)
from pricelab_core.infrastructure.http.enum.circuit_breaker_status import CircuitState
from pricelab_core.infrastructure.http.exception.circuit_breaker_open_exception import (
    CircuitBreakerOpenException,
)

P = ParamSpec("P")


class CircuitBreakerPolicy:
    def __init__(self, settings: CircuitBreakerSettings = CircuitBreakerSettings()):

        self._settings = settings
        self._state: CircuitState = CircuitState.CLOSED
        self._failure_counter: int = 0
        self._success_counter: int = 0
        self._last_failure_time: float = 0
        self._last_exception: Exception | None = None

    @property
    def last_exception(self) -> Exception | None:
        return self._last_exception

    @property
    def state(self) -> CircuitState:
        return self._state

    def _can_attempt(self) -> bool:

        # CLOSED
        if self._state == CircuitState.CLOSED:
            return True

        # OPEN
        if self._state == CircuitState.OPEN:
            return time.time() - self._last_failure_time > self._settings.recovery_timeout

        # HALF OPEN
        return True

    def _on_success(self) -> None:

        if self._state == CircuitState.HALF_OPEN:
            self._success_counter += 1
            if self._success_counter >= self._settings.success_threshold:
                self._state = CircuitState.CLOSED
                self._failure_counter = 0
                self._success_counter = 0
                self._last_exception = None

        else:
            self._failure_counter = 0

    def _on_failure(self, exception: Exception) -> None:

        self._failure_counter += 1
        self._last_failure_time = time.time()
        self._last_exception = exception

        if self._failure_counter >= self._settings.failure_threshold:
            self._state = CircuitState.OPEN

    async def call(self, func, *args: P.args, **kwargs: P.kwargs):

        if not self._can_attempt():
            raise CircuitBreakerOpenException(
                f"Circuit breaker open (last failure: {self._last_exception})"
            )

        if self._state == CircuitState.OPEN:
            self._state = CircuitState.HALF_OPEN

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as exception:
            self._on_failure(exception)
            raise
