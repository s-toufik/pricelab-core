from dataclasses import fields
from typing import Sequence, Tuple

from adapter.outbound.loguru.loguru_logger import LoguruLogger as Logger
from application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from application.port.outbound.sequence_analytics_engine import SequenceAnalyticsEngine
from domain.model.candles.candle import Candle
from domain.model.candles.candle_series import CandleSeries
from domain.model.analytics.analytics import Analytics
from domain.service.candles.candle_series_validator import CandleSeriesValidator
from domain.service.candles.candle_validator import CandleValidator


class AnalyseCandles(AnalyseSeriesUseCase):

    def __init__(self, computation_engine: SequenceAnalyticsEngine) -> None:
        self._computation_engine = computation_engine
        self._candle_validator = CandleValidator()
        self._candle_sequence_validator = CandleSeriesValidator()
        self._logger = Logger()

    def execute(self, candles: Sequence[Candle], params: dict) -> Tuple[Analytics, ...]:
        candle_series = CandleSeries()

        candle_series.symbol = candles[0].symbol
        candle_series.source = candles[0].source
        for candle in candles:
            if validat_candle := self._candle_validator.status(candle):
                high = candle.high
                low = candle.low
                close = candle.close
                candle_series.time.append(candle.timestamp)
                candle_series.open.append(candle.open)
                candle_series.high.append(high)
                candle_series.low.append(low)
                candle_series.close.append(close)
                candle_series.volumes.append(candle.volume)
                candle_series.typical_price.append((high + low + close)/3)
                candle_series.spread.append(high - low)
            else:
                self._logger.error(validat_candle.exception.__str__())

        if validat_candle_sequence := self._candle_sequence_validator.is_valid_for_analysis(candle_series):
            window = params.get('window', 2)
            symbol = candle_series.symbol
            source = candle_series.source
            time = self._computation_engine.to_array(candle_series.time)

            result = []
            for field in fields(CandleSeries):
                field_value = getattr(candle_series, field.name)
                if isinstance(field_value[0], float) and isinstance(field_value, Sequence):
                    result.append(
                        Analytics(
                            symbol=symbol,
                            source=source,
                            name=field.name,
                            time=time,
                            value=self._computation_engine.to_array(field_value),
                            log_returns=self._computation_engine.log_returns(field_value),
                            rolling_average=self._computation_engine.rolling_average(field_value, window = window),
                            rolling_standard_deviation=self._computation_engine.rolling_standard_deviation(field_value, window = window),
                            window=window
                        )
                    )
            return tuple(result)
        else:
            self._logger.error(validat_candle_sequence.exception.__str__())
            return (Analytics(),)