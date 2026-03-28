import threading
from typing import Sequence, TypeVar, Dict, Callable, cast, Tuple

from domain.model.quote import Quote
from domain.service.base_market_series_data import BaseMarketSeriesData

T = TypeVar('T')
class QuoteSeries(BaseMarketSeriesData):

    def __init__(self, elements: Sequence[Quote]):
        self._elements = elements
        self._cache: Dict[str, object] = {}
        self._lock = threading.RLock()

    def _get(self, field: str, func: Callable[[], T]) -> T:
        if not field in self._cache:
            while self._lock:
                if not field in self._cache:
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
        return self._get('times', lambda: tuple(element.timestamp for element in self._elements))

    @property
    def typical_prices(self) -> Tuple[float, ...]:
        return self._get('typical_price',
                  lambda: tuple((ask + bid)/2 for ask, bid in zip(self._ask_prices(), self._bid_prices()))
                  )

    @property
    def spread(self) -> Tuple[float, ...]:
        return self._get('spread',
                         lambda: tuple(ask - last for ask, last in zip(self._ask_prices(), self._last_prices()))
                         )

    @property
    def bid_prices(self) -> Tuple[float, ...]:
        return self._bid_prices()

    @property
    def ask_prices(self) -> Tuple[float, ...]:
        return self._ask_prices()

    @property
    def last_prices(self) -> Tuple[float, ...]:
        return self._last_prices()

    @property
    def volumes(self) -> Tuple[float, ...]:
        return self._get('volume', lambda: tuple(element.volume for element in self._elements))

    def _bid_prices(self) -> Tuple[float, ...]:
        return self._get('bid_price', lambda: tuple(element.bid for element in self._elements))

    def _last_prices(self) -> Tuple[float, ...]:
        return self._get('last_price', lambda: tuple(element.last for element in self._elements))

    def _ask_prices(self) -> Tuple[float, ...]:
        return self._get('ask_price', lambda: tuple(element.ask for element in self._elements))
