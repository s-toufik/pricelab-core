from dataclasses import fields
from typing import Sequence, Tuple

from application.ports.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from application.ports.outbound.sequence_analytics_engine import SequenceAnalyticsEngine
from domain.models.candles.candle import Candle
from domain.models.candles.candle_series import CandleSeries
from domain.models.analytics.analytics import Analytics
from domain.services.candles.candle_series_validator import CandleSeriesValidator
from domain.services.candles.candle_validator import CandleValidator


class AnalyseCandles(AnalyseSeriesUseCase):

    def __init__(self, computation_engine: SequenceAnalyticsEngine) -> None:
        self._computation_engine = computation_engine
        self._candle_validator = CandleValidator()
        self._candle_sequence_validator = CandleSeriesValidator()

    def execute(self, candles: Sequence[Candle], params: dict) -> Tuple[Analytics, ...]:
        sequence = CandleSeries()

        sequence.symbol = candles[0].symbol
        sequence.source = candles[0].source
        for candle in candles:
            if self._candle_validator.is_valid(candle):
                high = candle.high
                low = candle.low
                close = candle.close
                sequence.time.append(candle.timestamp)
                sequence.open.append(candle.open)
                sequence.high.append(high)
                sequence.low.append(low)
                sequence.close.append(close)
                sequence.volumes.append(candle.volume)
                sequence.typical_price.append((high + low + close)/3)
                sequence.spread.append(high - low)

        if self._candle_sequence_validator.is_valid_for_analysis(sequence):

            window = params.get('window', 2)
            symbol = sequence.symbol
            source = sequence.source
            time = self._computation_engine.to_array(sequence.time)

            result = []
            for field in fields(CandleSeries):
                field_value = getattr(sequence, field.name)
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
            return (Analytics(),)