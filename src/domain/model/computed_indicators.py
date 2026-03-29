from dataclasses import dataclass, fields
from typing import Sequence


@dataclass(frozen=True, slots=True)
class ComputedIndicators:
    time: Sequence[str]
    field: Sequence[float]
    returns: Sequence[float]
    rolling_average: Sequence[float]
    rolling_standard_deviation: Sequence[float]

    def __post_init__(self):
        lengths = {field.name: len(getattr(self, field.name)) for field in fields(self)}

        if len(set(lengths.values())) != 1:
            raise ValueError(
                f"All sequences must have the same length, got: {lengths}"
            )