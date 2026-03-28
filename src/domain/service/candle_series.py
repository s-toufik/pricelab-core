import threading
from typing import Sequence, Callable, TypeVar, cast, Tuple

from domain.model.candle import Candle
from domain.service.base_market_series_data import BaseMarketSeriesData

T = TypeVar('T')
class CandleSeries(BaseMarketSeriesData):

    def __init__(self, elements: Sequence[Candle]):
        self._elements = elements
        self._cache: dict[str, object] = {}
        self._lock = threading.RLock()

    def _get(self, field: str, func: Callable[[], T]) -> T:
        if field not in self._cache:
            print("1", field)
            with self._lock:
                print("2", field)
                if field not in self._cache:
                    self._cache[field] = func()

        return cast(T, self._cache[field])

    @property
    def symbol(self) -> str:
        return self._elements[0].symbol

    @property
    def source(self) -> str:
        return self._elements[0].source

    @property
    def time(self) -> Tuple[str, ...]:
        return self._get('times', lambda : tuple(element.timestamp for element in self._elements))

    @property
    def typical_prices(self) -> Tuple[float, ...]:
        return self._get('typical_price',
                         lambda:
                             tuple((high + low + close)/3 for high, low, close in
                             zip(self._high_prices(), self._low_prices(), self._close_prices())
                                   )
                         )

    @property
    def spread(self) -> Tuple[float, ...]:
        return self._get('spread',
                         lambda:
                             tuple(high - low for high, low
                             in zip(self._high_prices(), self._low_prices())
                         ))

    @property
    def open_prices(self) -> Tuple[float, ...]:
        return self._get('open_prices', lambda : tuple(element.open for element in self._elements))

    @property
    def high_prices(self) -> Tuple[float, ...]:
        return self._high_prices()

    @property
    def low_prices(self) -> Tuple[float, ...]:
        return self._low_prices()

    @property
    def close_prices(self) -> Tuple[float, ...]:
        return self._close_prices()

    @property
    def volumes(self) -> Tuple[float, ...]:
        return self._get('volumes', lambda : tuple(element.volume for element in self._elements))

    def _high_prices(self) -> Tuple[float, ...]:
        return self._get('high_prices', lambda : tuple(element.high for element in self._elements))

    def _low_prices(self) -> Tuple[float, ...]:
        return self._get('low_prices', lambda : tuple(element.low for element in self._elements))

    def _close_prices(self) -> Tuple[float, ...]:
        return self._get('close_prices', lambda : tuple(element.close for element in self._elements))
