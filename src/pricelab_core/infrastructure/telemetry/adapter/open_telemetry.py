from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Awaitable

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode, Tracer
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)

P = ParamSpec("P")
R = TypeVar("R")


class OpenTelemetryManager:
    def __init__(
        self,
        service_name: str,
        environment: RunTypeEnvironment = RunTypeEnvironment.debug,
        otlp_endpoint: str = "http://localhost:4317",
    ) -> None:

        self._service_name = service_name
        self._environment = environment

        resource = Resource.create(
            {
                SERVICE_NAME: service_name,
                "deployment.environment": environment.value,
            }
        )

        provider = TracerProvider(resource=resource)
        self._get_collector(environment, otlp_endpoint, provider)
        trace.set_tracer_provider(provider)
        self._provider = provider
        self._tracer: Tracer = trace.get_tracer(service_name)

    @staticmethod
    def _get_collector(
        environment: RunTypeEnvironment, otlp_endpoint: str, provider: TracerProvider
    ) -> None:
        if environment == RunTypeEnvironment.debug:
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

        else:
            provider.add_span_processor(
                BatchSpanProcessor(
                    OTLPSpanExporter(
                        endpoint=otlp_endpoint,
                        insecure=True,
                    )
                )
            )

    @property
    def tracer(self) -> Tracer:
        return self._tracer

    def shutdown(self) -> None:
        self._provider.shutdown()

    def trace(
        self, span_name: str
    ) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
        def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
            @wraps(func)
            async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                with self._tracer.start_as_current_span(span_name) as span:
                    self._enrich_span(span=span, args=args, kwargs=kwargs)
                    try:
                        result = await func(*args, **kwargs)
                        span.set_status(Status(StatusCode.OK))
                        return result

                    except Exception:
                        span.set_status(Status(StatusCode.ERROR))
                        raise

            return wrapper

        return decorator

    @staticmethod
    def _enrich_span(span, args, kwargs) -> None:

        method = kwargs.get("method")
        url = kwargs.get("url")

        if method:
            span.set_attribute(
                "http.method",
                method,
            )

        if url:
            span.set_attribute(
                "http.url",
                url,
            )
