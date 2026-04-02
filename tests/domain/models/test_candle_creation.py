from typing import Sequence

import pytest
from hypothesis import given

from domain.model.candles.candle import Candle
from tests.domain.models.candles_generator import candles_strategy

class TestCandleCreation:

    @given(candles = candles_strategy(min_size=1, max_size=1))
    def test_candle_field_type(self, candles: Sequence[Candle]) -> None:
        for candle in candles:
            assert isinstance(candle.source, str)
            assert isinstance(candle.symbol, str)
            assert isinstance(candle.timestamp, str)
            assert isinstance(candle.open, float)
            assert isinstance(candle.high, float)
            assert isinstance(candle.low, float)
            assert isinstance(candle.close, float)
            assert isinstance(candle.volume, float)

    @given(candles = candles_strategy(min_size=1, max_size=1))
    def test_candle_immutability(self, candles) -> None:
        with pytest.raises(AttributeError):
            for candle in candles:
                candle.open = 0.0

    @given(candles = candles_strategy(min_size=1, max_size=1))
    def test_candle_equality(self, candles: Sequence[Candle]) -> None:
        candle = candles[0]
        same_candle = Candle(
            source = candle.source,
            symbol = candle.symbol,
            timestamp = candle.timestamp,
            open = candle.open,
            high = candle.high,
            low = candle.low,
            close = candle.close,
            volume = candle.volume
        )
        assert candle == same_candle

    def test_candle(self) -> None:
        candle = Candle(
            source="binance",
            symbol="BTCUSDT",
            timestamp="2023-01-01T00:00:00",
            open=50000.0,
            high=50500.0,
            low=49500.0,
            close=50200.0,
            volume=1000.0
        )

        assert candle.source == "binance"
        assert candle.symbol == "BTCUSDT"