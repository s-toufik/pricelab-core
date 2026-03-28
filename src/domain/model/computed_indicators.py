from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class ComputedIndicators:
    time: Sequence[str]
    field: Sequence[float]
    returns: Sequence[float]
    rolling_average: Sequence[float]
    rolling_standard_deviation: Sequence[float]