from dataclasses import dataclass

from domain.models.base.base_market_data import BaseMarketData

@dataclass(frozen=True, slots=True)
class Quote(BaseMarketData):
    bid: float
    ask: float
    last: float
    volume: float