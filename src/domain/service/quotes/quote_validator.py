import datetime

from src.domain.dto.validation_status import ValidationStatus
from src.domain.model.quotes.quote import Quote


class QuoteValidator:

    def is_quote_valid(self, quote: Quote) -> ValidationStatus:

        if not (result := self._is_prices_positive(quote)).is_valid:
            return result

        if not (result := self._is_timestamp_valid(quote)).is_valid:
            return result

        if not (result := self._is_timestamp_valid(quote)).is_valid:
            return result

        return ValidationStatus.ok()

    @staticmethod
    def _is_prices_positive(quote: Quote) -> ValidationStatus:
        if not (quote.ask > 0 or quote.bid > 0 or quote.last > 0):
            ValidationStatus.fail("Prices must be positive", ValueError)
        return ValidationStatus.ok()

    @staticmethod
    def _is_prices_relation_valid(quote: Quote) -> ValidationStatus:
        if not (quote.bid < quote.ask):
            ValidationStatus.fail("Bid must be less than ask", ValueError)
        return ValidationStatus.ok()

    @staticmethod
    def _is_timestamp_valid(quote: Quote) -> ValidationStatus:
        if not isinstance(quote.timestamp, str):
            return ValidationStatus.fail("Timestamp must be a string", TypeError)

        try:
            datetime.datetime.fromisoformat(quote.timestamp)
        except ValueError:
            return ValidationStatus.fail("Timestamp must be ISO format", ValueError)

        return ValidationStatus.ok()
