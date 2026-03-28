from dataclasses import dataclass

from src.domain.model.base_market_data import BaseMarketData


@dataclass(frozen=True, slots=True)
class Quote(BaseMarketData):
    bid: float
    ask: float
    last: float
    volume: float

    def __post_init__(self):
        self._validate_prices()

    def _validate_prices(self):
        if self.ask < 0 or self.bid < 0 or self.last < 0:
            raise ValueError("Price must be non-negative")
        if self.bid > self.ask:
            raise ValueError("Bid cannot be greater than ask")

    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2

    def spread(self) -> float:
        return self.ask - self.bid
