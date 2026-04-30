from typing import Sequence, TypeVar

from pricelab_core.adapter.outbound.logger.logger_instance import logger
from pricelab_core.application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.quotes.quote import Quote

T = TypeVar("T", Sequence[Candle], Sequence[Quote])
class AnalyticsCLI:
    def __init__(self, use_case: AnalyseSeriesUseCase, params: dict = None) -> None:
        self._use_case = use_case
        self._params = params if params is not None else {}
        self._logger = logger

    def run(self, sequence: T) -> None:
        result = self._use_case.execute(sequence, self._params)
        self._logger.info(result.__str__())
