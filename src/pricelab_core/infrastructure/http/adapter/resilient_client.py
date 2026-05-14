from typing import ParamSpec, Final, Any

from pricelab_core.infrastructure.http.enum.http_method import HttpMethod
from pricelab_core.infrastructure.http.port.circuit_breaker import CircuitBreaker
from pricelab_core.infrastructure.http.port.http_client import HttpClient
from pricelab_core.infrastructure.http.port.retry import Retry
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry

P = ParamSpec("P")


class ResilientClient:
    def __init__(
        self,
        base_client: HttpClient,
        circuit_breaker: CircuitBreaker,
        retry_policy: Retry,
        trace_manager: Telemetry,
    ) -> None:

        self._base_client: Final = base_client
        self._circuit_breaker: Final = circuit_breaker
        self._retry: Final = retry_policy
        self._trace: Final = trace_manager

        self.get = self._build_pipeline(
            method_name=HttpMethod.GET.value, method=self._base_client.get
        )
        self.post = self._build_pipeline(
            method_name=HttpMethod.POST.value, method=self._base_client.post
        )

    def _build_pipeline(self, method_name: str, method) -> Any:

        @self._trace.trace(method_name)
        @self._retry.decorator
        async def wrapped(*args: P.args, **kwargs: P.kwargs):

            async def execute():
                return await method(*args, **kwargs)

            return await self._circuit_breaker.call(execute)

        return wrapped
