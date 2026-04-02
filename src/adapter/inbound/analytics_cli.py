from typing import Sequence, TypeVar

from adapter.outbound.loguru.loguru_logger import LoguruLogger as Logger
from application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from domain.model.candles.candle import Candle
from domain.model.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])
class AnalyticsCLI:
    def __init__(self, use_case: AnalyseSeriesUseCase, params: dict = None) -> None:
        self._use_case = use_case
        self._params = params if params is not None else {}
        self.logger = Logger()

    def run(self, sequence: T) -> None:
        result = self._use_case.execute(sequence, self._params)
        self.logger.info(result.__str__())