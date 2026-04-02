from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class PredictionSeries:
    symbol: str = ""
    source: str = ""
    time: List[str] = field(default_factory=list)
    predicted_prices: List[float] = field(default_factory=list)
    confidences: List[float] = field(default_factory=list)
    horizon: List[float] = field(default_factory=list)
