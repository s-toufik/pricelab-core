from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class Analytics:
    source: str | None = None
    symbol: str | None = None
    name: str | None = None
    time: Sequence[str] | None = None
    value: Sequence[float] | None = None
    log_returns: Sequence[float] | None = None
    rolling_average: Sequence[float] | None = None
    rolling_standard_deviation: Sequence[float] | None = None
    window: int | None = None