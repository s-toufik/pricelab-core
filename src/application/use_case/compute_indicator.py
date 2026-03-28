from typing import Sequence, TypeAlias, Callable

from domain.model.computed_indicators import ComputedIndicators
from domain.service.candle_series import CandleSeries
from domain.service.quote_series import QuoteSeries
from port.outbound.series_computation import SeriesComputation

Series : TypeAlias = CandleSeries | QuoteSeries
Accessor : TypeAlias = Callable[[Series], Sequence[float]]

class ComputeIndicator:

    def __init__(self, series: Series, compute_engine: SeriesComputation):
        self._series = series
        self._compute_engine = compute_engine

    def execute(self, accessor: Accessor, windows: int = 5) -> ComputedIndicators:
        data = accessor(self._series)
        array = self._compute_engine.field(data)
        return ComputedIndicators(
            time = self._series.time,
            field = array,
            returns=self._compute_engine.returns(array),
            rolling_average=self._compute_engine.rolling_average(array, windows),
            rolling_standard_deviation=self._compute_engine.rolling_standard_deviation(array, windows)
        )