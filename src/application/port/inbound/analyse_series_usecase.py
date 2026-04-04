from abc import ABC, abstractmethod
from typing import Sequence, TypeVar

from src.domain.model.analytics.analytics import Analytics
from src.domain.model.candles.candle import Candle
from src.domain.model.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])


class AnalyseSeriesUseCase(ABC):

    @abstractmethod
    def execute(self, sequence: T, params: dict) -> Sequence[Analytics]:
        pass
