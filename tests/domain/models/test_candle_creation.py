import pytest

from domain.model.candles.candle import Candle
from tests.domain.models.candles_generator import candles_strategy

class TestCandleCreation:

    @pytest.fixture
    def candle_init(self) -> Candle:
        candles = candles_strategy(min_size=1, max_size=1).example()
        return candles[0]

    def test_candle_field_type(self, candle_init: Candle) -> None:
        assert isinstance(candle_init.source, str)
        assert isinstance(candle_init.symbol, str)
        assert isinstance(candle_init.timestamp, str)
        assert isinstance(candle_init.open, float)
        assert isinstance(candle_init.high, float)
        assert isinstance(candle_init.low, float)
        assert isinstance(candle_init.close, float)
        assert isinstance(candle_init.volume, float)

    def test_candle_immutability(self, candle_init) -> None:
        with pytest.raises(AttributeError):
            candle_init.open = 0.0

    def test_candle_equality(self, candle_init) -> None:
        same_candle = Candle(
            source = candle_init.source,
            symbol = candle_init.symbol,
            timestamp = candle_init.timestamp,
            open = candle_init.open,
            high = candle_init.high,
            low = candle_init.low,
            close = candle_init.close,
            volume = candle_init.volume
        )
        assert candle_init == same_candle

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