from dataclasses import fields
from typing import Sequence, Tuple


from pricelab_core.infrastructure.computation_engine.port.engine import Engine
from pricelab_core.infrastructure.logger.port.logger import Logger
from pricelab_core.domain.base.const_typing import Kind
from pricelab_core.domain.model.analytics.analytics import Analytics
from pricelab_core.domain.model.quotes.quote import Quote
from pricelab_core.domain.model.quotes.quote_series import QuoteSeries
from pricelab_core.domain.service.quotes.quote_series_validator import QuoteSeriesValidator
from pricelab_core.domain.service.quotes.quote_validator import QuoteValidator


class AnalyseQuotesUseCase:
    def __init__(self, computation_engine: Engine, logger: Logger) -> None:
        self._computation_engine = computation_engine
        self._logger = logger
        self._quote_validator = QuoteValidator()
        self._quote_sequence_validator = QuoteSeriesValidator()

    def execute(self, sequence: Sequence[Quote], params: dict) -> Tuple[Analytics, ...]:
        quote_series = QuoteSeries()

        quote_series.symbol = sequence[0].symbol
        quote_series.source = sequence[0].source
        for quote in sequence:
            if validat_quote := self._quote_validator.is_quote_valid(quote):
                ask = quote.ask
                bid = quote.bid
                last = quote.last
                quote_series.time.append(quote.timestamp)
                quote_series.bid.append(bid)
                quote_series.ask.append(ask)
                quote_series.last.append(last)
                quote_series.volumes.append(quote.volume)
                quote_series.typical_price.append((ask + bid) / 2)
                quote_series.spread.append(ask - last)
            else:
                self._logger.error(validat_quote.exception.__str__())

        if validat_quote_sequence := self._quote_sequence_validator.is_valid_for_analysis(
            quote_series
        ):
            window = params.get("window", 2)
            kind: Kind = params.get("kind", "linear")  # type: ignore
            dx = params.get("dx", 0.2)
            symbol = quote_series.symbol
            source = quote_series.source
            time = quote_series.time

            result = []
            for field in fields(QuoteSeries):
                field_value = getattr(quote_series, field.name)
                if isinstance(field_value[0], float) and isinstance(field_value, Sequence):
                    result.append(
                        Analytics(
                            symbol=symbol,
                            source=source,
                            name=field.name,
                            time=time,
                            value=list(self._computation_engine.arithmetic.to_array(field_value)),
                            log_returns=list(
                                self._computation_engine.arithmetic.log_returns(field_value)
                            ),
                            rolling_average=list(
                                self._computation_engine.arithmetic.rolling_average(
                                    field_value, window=window
                                )
                            ),
                            rolling_standard_deviation=list(
                                self._computation_engine.arithmetic.rolling_standard_deviation(
                                    field_value, window=window
                                )
                            ),
                            interpolation=list(
                                self._computation_engine.calculus.interpolate(
                                    field_value, kind=kind
                                )
                            ),
                            integration=self._computation_engine.calculus.integrate(
                                field_value, dx=dx
                            ),
                        )
                    )
            return tuple(result)
        else:
            self._logger.error(validat_quote_sequence.exception.__str__())
            return (Analytics(),)
