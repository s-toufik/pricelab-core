import datetime

from domain.models.quotes.quote import Quote

class QuoteValidator:

    def is_quote_valid(self, quote: Quote) -> bool:
        return (self._is_prices_positive(quote) and
                self._is_prices_relation_valid(quote) and
                self._is_timestamp_valid(quote))

    @staticmethod
    def _is_prices_positive(quote: Quote) -> bool:
        return quote.ask > 0 or quote.bid > 0 or quote.last > 0

    @staticmethod
    def _is_prices_relation_valid(quote: Quote) -> bool:
        return quote.bid < quote.ask

    @staticmethod
    def _is_timestamp_valid(quote: Quote) -> bool:
        if not isinstance(quote.timestamp, str):
            TypeError("Timestamp must be a string")
            return False
        try:
            datetime.datetime.fromisoformat(quote.timestamp)
            return True
        except ValueError:
            ValueError("Timestamp must be a string")
            return False