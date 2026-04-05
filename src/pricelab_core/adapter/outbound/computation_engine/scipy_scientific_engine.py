import numbers
from typing import Sequence, TypeVar, Any, Literal, Union

import numpy as np
from scipy import interpolate, integrate

from src.pricelab_core.application.port.outbound.computation_engine.scientifc_computation_engine import ScientificEngine

Numeric = TypeVar("Numeric", bound=numbers.Real)
Kind = Union[
    Literal["linear", "nearest", "nearest-up", "zero", "slinear", "quadratic", "cubic", "previous", "next"],
    int
]


class ScipyScientificEngine(ScientificEngine):

    def _to_array(self, sequence: Sequence[Any]) -> np.ndarray:
        return np.asarray(sequence, dtype=np.float64)

    def integrate(self, sequence: Sequence[Numeric], dx: float) -> float:
        arr = self._to_array(sequence)
        return float(integrate.trapezoid(arr, dx=dx))

    def interpolate(self, sequence: Sequence[Numeric], kind: Kind = "linear") -> Sequence[Numeric]:
        arr = self._to_array(sequence)
        x = np.arange(len(arr))
        f = interpolate.interp1d(x, arr, kind=kind)
        return f(x)
