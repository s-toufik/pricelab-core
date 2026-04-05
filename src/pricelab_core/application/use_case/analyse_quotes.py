from dataclasses import fields
from typing import Sequence, Tuple

from pricelab_core.adapter.outbound.computation_engine.start_compute_engine import StartComputeEngine
from pricelab_core.adapter.outbound.logger.loguru_logger import LoguruLogger as Logger
from pricelab_core.application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from pricelab_core.domain.model.analytics.analytics import Analytics
from pricelab_core.domain.model.quotes.quote import Quote
from pricelab_core.domain.model.quotes.quote_series import QuoteSeries
from pricelab_core.domain.service.quotes.quote_series_validator import QuoteSeriesValidator
from pricelab_core.domain.service.quotes.quote_validator import QuoteValidator


class AnalyseQuotes(AnalyseSeriesUseCase):

    def __init__(self) -> None:
        self._computation_engine = StartComputeEngine().engine
        self._quote_validator = QuoteValidator()
        self._quote_sequence_validator = QuoteSeriesValidator()
        self._logger = Logger()

    def execute(self, quotes: Sequence[Quote], params: dict) -> Tuple[Analytics, ...]:
        sequence = QuoteSeries()

        sequence.symbol = quotes[0].symbol
        sequence.source = quotes[0].source
        for quote in quotes:
            if validat_quote := self._quote_validator.is_quote_valid(quote):
                ask = quote.ask
                bid = quote.bid
                last = quote.last
                sequence.time.append(quote.timestamp)
                sequence.bid.append(bid)
                sequence.ask.append(ask)
                sequence.last.append(last)
                sequence.volumes.append(quote.volume)
                sequence.typical_price.append((ask + bid) / 2)
                sequence.spread.append(ask - last)
            else:
                self._logger.error(validat_quote.exception.__str__())

        if validat_quote_sequence := self._quote_sequence_validator.is_valid_for_analysis(sequence):
            window = params.get('window', 2)
            kind = params.get('kind', 'linear')
            dx = params.get('dx', 0.2)
            symbol = sequence.symbol
            source = sequence.source
            time = sequence.time

            result = []
            for field in fields(QuoteSeries):
                field_value = getattr(sequence, field.name)
                if isinstance(field_value[0], float) and isinstance(field_value, Sequence):
                    result.append(
                        Analytics(
                            symbol=symbol,
                            source=source,
                            name=field.name,
                            time=time,
                            value=list(self._computation_engine.to_array(field_value)),
                            log_returns=list(self._computation_engine.log_returns(field_value)),
                            rolling_average=list(self._computation_engine.rolling_average(field_value, window=window)),
                            rolling_standard_deviation=list(self._computation_engine.rolling_standard_deviation(field_value,window=window)),
                            interpolation=list(self._computation_engine.interpolate(field_value, kind=kind)),
                            integration=self._computation_engine.integrate(field_value, dx=dx)
                        )
                    )
            return tuple(result)
        else:
            self._logger.error(validat_quote_sequence.exception.__str__())
            return (Analytics(),)
