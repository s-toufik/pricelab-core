from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BaseMarketData:
    source: str
    symbol: str
    timestamp: str
