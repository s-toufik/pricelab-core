from dataclasses import dataclass
from typing import Tuple, Type


@dataclass(slots=True)
class RetrySettings:
    retries: int = 4
    base_delay: float = 0.1
    retry_on: Tuple[Type[Exception], ...] = (Exception,)
