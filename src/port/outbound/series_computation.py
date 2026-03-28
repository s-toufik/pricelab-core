from abc import ABC, abstractmethod
from typing import Sequence


class SeriesComputation(ABC):

    @abstractmethod
    def field(self, sequence: Sequence[float]) -> Sequence[float]:
        pass

    @abstractmethod
    def returns(self, sequence: Sequence[float]) -> Sequence[float]:
        pass

    @abstractmethod
    def rolling_average(self, sequence: Sequence[float], window: int) -> Sequence[float]:
        pass

    @abstractmethod
    def rolling_standard_deviation(self, sequence: Sequence[float], window: int) -> Sequence[float]:
        pass