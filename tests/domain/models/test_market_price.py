import pytest
from dataclasses import FrozenInstanceError
from hypothesis import given, strategies as st

from src.domain.models.market_price import MarketPrice


class TestMarketPrice:

    def test_market_price_creation(self):
        price = MarketPrice(
            source="foo",
            symbol="BAR",
            timestamp=1,
            bid=1,
            ask=2,
            last=0.5,
            volume=10
        )
        assert price.source == "foo"
        assert price.symbol == "BAR"
        assert price.bid == 1
        assert price.ask == 2


    def test_negative_price(self):
        with pytest.raises(ValueError):
            MarketPrice(source="foo", symbol="BAR", timestamp=1, bid=-1, ask=2, last=0.5, volume=10)
            MarketPrice(source="foo", symbol="BAR", timestamp=1, bid=1, ask=-2, last=0.5, volume=10)
            MarketPrice(source="foo", symbol="BAR", timestamp=1, bid=1, ask=2, last=-0.5, volume=10)

    def test_bid_greater_than_ask_raises(self):
        with pytest.raises(ValueError):
            MarketPrice("foo", "BAR", 1, 105, 100, 102, 10)

    def test_mid_price(self):
        price = MarketPrice("foo", "BAR", 1, 100, 102, 101, 10)
        assert price.mid_price() == 101

    def test_spread(self):
        price = MarketPrice("foo", "BAR", 1, 100, 102, 101, 10)
        assert price.spread() == 2

    def test_market_price_is_immutable(self):
        price = MarketPrice("foo", "BAR", 1, 100, 101, 100, 10)
        with pytest.raises(FrozenInstanceError):
            price.bid = 200

    @given(
        bid=st.floats(min_value=0, max_value=1e6),
        spread=st.floats(min_value=0, max_value=1e5)
    )
    def test_bid_leq_ask_property(self, bid, spread):
        ask = bid + spread
        price = MarketPrice("foo", "BAR", 1, bid, ask, bid, 10)
        assert price.bid <= price.ask

    @given(
        bid=st.floats(min_value=0, max_value=1e6),
        spread=st.floats(min_value=0, max_value=1e5)
    )
    def test_mid_price_within_bid_ask(self, bid, spread):
        ask = bid + spread
        price = MarketPrice("foo", "BAR", 1, bid, ask, bid, 10)
        mid = price.mid_price()
        assert bid <= mid <= ask

    @given(
        bid=st.floats(min_value=0, max_value=1e6),
        spread=st.floats(min_value=0, max_value=1e5)
    )
    def test_spread_formula_property(self, bid, spread):
        ask = bid + spread
        price = MarketPrice("foo", "BAR", 1, bid, ask, bid, 10)
        assert price.spread() - spread < 1e-6