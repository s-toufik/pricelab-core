from abc import ABC, abstractmethod
from typing import Sequence


class BaseMarketSeriesData(ABC):

    @property
    @abstractmethod
    def time(self) -> Sequence[str]:
        pass

    @property
    @abstractmethod
    def typical_prices(self) -> Sequence[float]:
        pass

    @property
    @abstractmethod
    def spread(self) -> Sequence[float]:
        pass
