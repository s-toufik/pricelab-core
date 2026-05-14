from typing import Protocol, Callable, Awaitable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class Telemetry(Protocol):
    def trace(
        self, span_name: str
    ) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...
    def shutdown(self) -> None: ...
