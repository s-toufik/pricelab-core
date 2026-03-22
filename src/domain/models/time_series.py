import numpy as np
from typing import List

from src.domain.models.market_price import MarketPrice

class TimeSeries:
    __slots__ = ("_prices",)

    def __init__(self, prices: List[MarketPrice]):
        if not prices:
            raise ValueError("TimeSeries cannot be empty")
        self._prices = prices

    def mid_prices(self) -> np.ndarray:
        return np.array(
            [mid_price.mid_price() for mid_price in self._prices],
            dtype=np.float64
        )

    def log_return(self) -> np.ndarray:
        return np.diff(
            np.log(
                self.mid_prices()
            )
        )

    def volatility(self) -> float:
        return float(
            np.std(
                self.log_return()
            )
        )