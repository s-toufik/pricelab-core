from dataclasses import dataclass

from domain.model.base_market_data import BaseMarketData


@dataclass(frozen=True, slots=True)
class Candle(BaseMarketData):
    open: float
    high: float
    low: float
    close: float
    volume: float
