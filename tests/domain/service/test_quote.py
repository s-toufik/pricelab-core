from hypothesis import given
from hypothesis.strategies import SearchStrategy

from domain.model.quote import Quote
from tests.domain.service.test_series_helper import build_quote

quote_strategy: SearchStrategy[Quote] = build_quote()  # type: ignore

class TestQuote:

    @given(quote=quote_strategy)
    def test_quote_invariants(self, quote: Quote):
        assert quote.bid <= quote.ask
        assert quote.bid <= quote.last <= quote.ask
        assert quote.spread() >= 0

