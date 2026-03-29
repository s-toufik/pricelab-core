from abc import ABC, abstractmethod
from typing import Sequence, TypeVar

from domain.models.analytics.analytics import Analytics
from domain.models.candles.candle import Candle
from domain.models.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])
class AnalyseSeriesUseCase(ABC):

    @abstractmethod
    def execute(self, sequence: T, params: dict) -> Sequence[Analytics]:
        pass