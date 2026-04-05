from abc import ABC, abstractmethod
from typing import Sequence, TypeVar

from pricelab_core.domain.model.analytics.analytics import Analytics
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])


class AnalyseSeriesUseCase(ABC):

    @abstractmethod
    def execute(self, sequence: T, params: dict) -> Sequence[Analytics]:
        pass
