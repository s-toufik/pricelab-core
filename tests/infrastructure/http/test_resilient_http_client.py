import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Any

from pricelab_core.infrastructure.http.adapter.resilient_client import ResilientClient
from pricelab_core.infrastructure.http.configuration.circuite_breaker_configuration import (
    CircuitBreakerSettings,
)
from pricelab_core.infrastructure.http.configuration.retry_configuration import RetrySettings
from pricelab_core.infrastructure.http.port.http_client import HttpClient
from pricelab_core.infrastructure.http.port.circuit_breaker import CircuitBreaker
from pricelab_core.infrastructure.http.port.retry import Retry
from pricelab_core.infrastructure.telemetry.port.telemetry import Telemetry


class MockHttpClient(HttpClient):
    async def start(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def get(self, endpoint: str, *, params=None, headers=None) -> Any:
        return {"ok": True}

    async def post(self, endpoint: str, *, body=None, headers=None) -> Any:
        return {"ok": True}


class MockCircuitBreaker(CircuitBreaker):
    @property
    def settings(self) -> CircuitBreakerSettings:
        return CircuitBreakerSettings()

    def _can_attempt(self) -> bool:
        return True

    def _on_success(self) -> None:
        pass

    def _on_failure(self, exception: Exception) -> None:
        pass

    async def call(self, func, *args, **kwargs):
        return await func()


class MockRetry(Retry):
    @property
    def settings(self) -> RetrySettings:
        return RetrySettings()

    def decorator(self, func):
        return func  # passthrough


class MockTelemetry(Telemetry):
    def trace(self, span_name, static_attributes):
        def decorator(func):
            return func  # passthrough

        return decorator

    def shutdown(self) -> None:
        pass


@pytest.fixture
def resilient_client():
    return ResilientClient(
        base_client=MockHttpClient(),
        circuit_breaker=MockCircuitBreaker(),
        retry_policy=MockRetry(),
        trace_manager=MockTelemetry(),
    )


@pytest.mark.asyncio
async def test_start_and_close(resilient_client):
    await resilient_client.start()
    await resilient_client.close()


@pytest.mark.asyncio
async def test_get_returns_response(resilient_client):
    result = await resilient_client.get(endpoint="/health")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_post_returns_response(resilient_client):
    result = await resilient_client.post(endpoint="/health")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_circuit_breaker_is_called():
    cb = MockCircuitBreaker()
    cb.call = AsyncMock(return_value={"ok": True})

    client = ResilientClient(
        base_client=MockHttpClient(),
        circuit_breaker=cb,
        retry_policy=MockRetry(),
        trace_manager=MockTelemetry(),
    )

    await client.get(endpoint="/health")
    cb.call.assert_called_once()


@pytest.mark.asyncio
async def test_retry_decorator_is_applied():
    retry = MockRetry()
    retry.decorator = MagicMock(side_effect=lambda f: f)

    ResilientClient(
        base_client=MockHttpClient(),
        circuit_breaker=MockCircuitBreaker(),
        retry_policy=retry,
        trace_manager=MockTelemetry(),
    )

    # decorator is called once per method (get + post)
    assert retry.decorator.call_count == 2


@pytest.mark.asyncio
async def test_telemetry_trace_is_applied():
    telemetry = MockTelemetry()
    telemetry.trace = MagicMock(side_effect=lambda **kwargs: lambda f: f)

    ResilientClient(
        base_client=MockHttpClient(),
        circuit_breaker=MockCircuitBreaker(),
        retry_policy=MockRetry(),
        trace_manager=telemetry,
    )

    # trace is called once per method (get + post)
    assert telemetry.trace.call_count == 2


@pytest.mark.asyncio
async def test_circuit_breaker_failure_propagates():
    cb = MockCircuitBreaker()
    cb.call = AsyncMock(side_effect=RuntimeError("circuit open"))

    client = ResilientClient(
        base_client=MockHttpClient(),
        circuit_breaker=cb,
        retry_policy=MockRetry(),
        trace_manager=MockTelemetry(),
    )

    with pytest.raises(RuntimeError, match="circuit open"):
        await client.get(endpoint="/health")
