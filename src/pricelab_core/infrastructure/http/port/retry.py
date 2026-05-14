from typing import Protocol, ParamSpec, TypeVar, Callable, Awaitable

P = ParamSpec("P")
R = TypeVar("R")


class Retry(Protocol):
    def decorator(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]: ...
