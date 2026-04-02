from abc import ABC, abstractmethod
from typing import Sequence, TypeVar

from domain.model.analytics.analytics import Analytics
from domain.model.candles.candle import Candle
from domain.model.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])
class AnalyseSeriesUseCase(ABC):

    @abstractmethod
    def execute(self, sequence: T, params: dict) -> Sequence[Analytics]:
        pass