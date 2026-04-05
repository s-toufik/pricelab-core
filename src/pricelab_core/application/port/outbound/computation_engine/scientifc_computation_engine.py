import numbers
from abc import ABC, abstractmethod
from typing import Sequence, TypeVar

Numeric = TypeVar("Numeric", bound=numbers.Real)


class ScientificEngine(ABC):

    @abstractmethod
    def integrate(self, sequence: Sequence[Numeric], dx: float) -> float:
        pass

    @abstractmethod
    def interpolate(self, sequence: Sequence[Numeric], kind: str = "linear") -> Sequence[Numeric]:
        pass
