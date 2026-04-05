from dataclasses import dataclass

from src import BaseMarketData


@dataclass(frozen=True, slots=True)
class Prediction(BaseMarketData):
    predicted_price: float
    confidence: float
    horizon: int
