from pprint import pprint
from typing import Sequence, TypeVar

from application.ports.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from domain.models.candles.candle import Candle
from domain.models.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])
class AnalyticsCLI:
    def __init__(self, use_case: AnalyseSeriesUseCase, params: dict = None) -> None:
        self._use_case = use_case
        self._params = params if params is not None else {}

    def run(self, sequence: T) -> None:
        result = self._use_case.execute(sequence, self._params)
        pprint(result, indent=2)