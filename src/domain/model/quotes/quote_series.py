from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class QuoteSeries:
    symbol: str = ""
    source: str = ""
    time: List[str] = field(default_factory=list)
    bid: List[float] = field(default_factory=list)
    ask: List[float] = field(default_factory=list)
    last: List[float] = field(default_factory=list)
    volumes: List[float] = field(default_factory=list)
    typical_price: List[float] = field(default_factory=list)
    spread: List[float] = field(default_factory=list)