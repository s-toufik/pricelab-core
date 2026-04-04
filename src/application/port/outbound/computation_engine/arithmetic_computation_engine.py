import numbers
from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Any

Numeric = TypeVar("Numeric", bound=numbers.Real)


class ArithmeticEngine(ABC):

    @abstractmethod
    def to_array(self, sequence: Sequence[Any]) -> Sequence[Any]:
        pass

    @abstractmethod
    def log_returns(self, sequence: Sequence[Numeric]) -> Sequence[Numeric]:
        pass

    @abstractmethod
    def rolling_average(self, sequence: Sequence[Numeric], window: int) -> Sequence[Numeric]:
        pass

    @abstractmethod
    def rolling_standard_deviation(self, sequence: Sequence[Numeric], window: int) -> Sequence[Numeric]:
        pass
