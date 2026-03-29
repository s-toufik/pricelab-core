from dataclasses import dataclass

from domain.models.base.base_market_data import BaseMarketData


@dataclass(frozen=True, slots=True)
class Prediction(BaseMarketData):
    predicted_price: float
    confidence: float
    horizon: int