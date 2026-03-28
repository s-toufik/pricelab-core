import threading
from typing import Sequence, TypeVar, Dict, Callable, cast, Tuple

from domain.model.prediction import Prediction

T = TypeVar("T")
class PredictionSeries:

    def __init__(self, elements: Sequence[Prediction]):
        self._elements = elements
        self._cache: Dict[str, object] = {}
        self._lock = threading.Lock()

    def _get(self, field: str, fun: Callable[[], T]) -> T:
        if not field in self._cache:
            with self._lock:
                if not field in self._cache:
                    self._cache[field] = fun()

        return cast(T, self._cache[field])

    @property
    def symbol(self) -> str:
        return self._elements[0].symbol

    @property
    def source(self) -> str:
        return self._elements[0].source

    @property
    def times(self) -> Tuple[str, ...]:
        return self._get('times', lambda: tuple(element.timestamp for element in self._elements))

    @property
    def prediction_prices(self) -> Tuple[float, ...]:
        return self._get('prediction_prices', lambda : tuple(element.predicted_price for element in self._elements))

    @property
    def confidences(self) -> Tuple[float, ...]:
        return self._get('confidence', lambda: tuple(element.confidence for element in self._elements))

    @property
    def horizons(self) -> Tuple[float, ...]:
        return self._get('horizon', lambda: tuple(element.horizon for element in self._elements))
