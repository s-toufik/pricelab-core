from dataclasses import fields
from typing import Sequence, Tuple

from adapter.outbound.loguru.loguru_logger import LoguruLogger as Logger
from application.port.inbound.analyse_series_usecase import AnalyseSeriesUseCase
from application.port.outbound.sequence_analytics_engine import SequenceAnalyticsEngine
from domain.model.analytics.analytics import Analytics
from domain.model.quotes.quote import Quote
from domain.model.quotes.quote_series import QuoteSeries
from domain.service.quotes.quote_series_validator import QuoteSeriesValidator
from domain.service.quotes.quote_validator import QuoteValidator

class AnalyseQuotes(AnalyseSeriesUseCase):

    def __init__(self, computation_engine: SequenceAnalyticsEngine) -> None:
        self._computation_engine = computation_engine
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

        if validat_quote_sequence:= self._quote_sequence_validator.is_valid_for_analysis(sequence):
            window = params.get('window', 2)
            symbol = sequence.symbol
            source = sequence.source
            time = self._computation_engine.to_array(sequence.time)

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
                            value=self._computation_engine.to_array(field_value),
                            log_returns=self._computation_engine.log_returns(field_value),
                            rolling_average=self._computation_engine.rolling_average(field_value, window = window),
                            rolling_standard_deviation=self._computation_engine.rolling_standard_deviation(field_value, window = window),
                            window=window
                        )
                    )
            return tuple(result)
        else:
            self._logger.error(validat_quote_sequence.exception.__str__())
            return (Analytics(),)

