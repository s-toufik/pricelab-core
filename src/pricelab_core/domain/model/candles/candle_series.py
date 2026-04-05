from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class CandleSeries:
    symbol: str = ""
    source: str = ""
    time: List[str] = field(default_factory=list)
    open: List[float] = field(default_factory=list)
    high: List[float] = field(default_factory=list)
    low: List[float] = field(default_factory=list)
    close: List[float] = field(default_factory=list)
    volumes: List[float] = field(default_factory=list)
    typical_price: List[float] = field(default_factory=list)
    spread: List[float] = field(default_factory=list)
