from dataclasses import fields
from typing import Sequence, Tuple

from pricelab_core.adapter.outbound.computation_engine.start_compute_engine import StartComputeEngine
from pricelab_core.adapter.outbound.logger.loguru_logger import LoguruLogger as Logger
from pricelab_core.application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from pricelab_core.domain.model.analytics.analytics import Analytics
from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.model.candles.candle_series import CandleSeries
from pricelab_core.domain.service.candles.candle_series_validator import CandleSeriesValidator
from pricelab_core.domain.service.candles.candle_validator import CandleValidator


class AnalyseCandles(AnalyseSeriesUseCase):

    def __init__(self) -> None:
        self._computation_engine = StartComputeEngine().engine
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
                candle_series.typical_price.append((high + low + close) / 3)
                candle_series.spread.append(high - low)
            else:
                self._logger.error(validat_candle.exception.__str__())

        if validat_candle_sequence := self._candle_sequence_validator.is_valid_for_analysis(candle_series):
            window = params.get('window', 2)
            kind = params.get('kind', 'linear')
            dx = params.get('dx', 0.2)
            symbol = candle_series.symbol
            source = candle_series.source
            time = candle_series.time

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
                            value=field_value,
                            log_returns=list(self._computation_engine.log_returns(field_value)),
                            rolling_average=list(self._computation_engine.rolling_average(field_value, window=window)),
                            rolling_standard_deviation=list(self._computation_engine.rolling_standard_deviation(field_value,window=window)),
                            interpolation=list(self._computation_engine.interpolate(field_value, kind=kind)),
                            integration=self._computation_engine.integrate(field_value, dx=dx)
                        )
                    )
            return tuple(result)
        else:
            self._logger.error(validat_candle_sequence.exception.__str__())
            return (Analytics(),)
