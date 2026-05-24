from dataclasses import dataclass
from typing import Tuple, Type


@dataclass(frozen=True, slots=True)
class RetrySettings:
    retries: int = 4
    base_delay: float = 0.1
    retry_on: Tuple[Type[Exception], ...] = (Exception,)

    def __post_init__(self):
        if not self.retry_on:
            raise RuntimeError("retry_on cannot be empty")
