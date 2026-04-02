from enum import auto, Enum
from typing import Sequence

from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy

from domain.model.base.base_market_data import BaseMarketData
from domain.model.candles.candle import Candle

class InvalidCandleReason(Enum):
    INVALID_TIMESTAMP = auto()
    NEGATIVE_VOLUME = auto()
    LOW_GREATER_THAN_HIGH = auto()
    OPEN_OUTSIDE_RANGE = auto()
    CLOSE_OUTSIDE_RANGE = auto()


def base_market_data_strategy() -> SearchStrategy[BaseMarketData]:
    return st.builds(
        BaseMarketData,
        source=st.sampled_from(["binance", "coinbase", "kraken"]),
        symbol=st.sampled_from(["BTCUSDT", "ETHUSDT", "AAPL", "TSLA"]),
        timestamp=st.datetimes().map(lambda dt: dt.isoformat()),
    )

@st.composite
def candle_strategy(draw) -> Candle:

    base_price = st.floats(min_value=0.01, max_value=1e6, allow_nan=False, allow_infinity=False)
    spread = st.floats(min_value=0.0, max_value=1000, allow_nan=False, allow_infinity=False)
    base = draw(base_market_data_strategy())
    price = draw(base_price)
    delta_high = draw(spread)
    delta_low = draw(spread)

    low = price - delta_low
    high = price + delta_high

    open_ = draw(st.floats(min_value=low, max_value=high))
    close = draw(st.floats(min_value=low, max_value=high))
    volume = draw(st.floats(min_value=0, max_value=1e9))

    return Candle(
        source=base.source,
        symbol=base.symbol,
        timestamp=base.timestamp,
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )

@st.composite
def invalid_candle_strategy(draw, reason: InvalidCandleReason | None = None) -> Candle | None:
    base = draw(base_market_data_strategy())
    price = draw(st.floats(min_value=0.01, max_value=1e6, allow_nan=False, allow_infinity=False))
    spread = draw(st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False))

    low = price - spread
    high = price + spread

    if reason is None:
        reason = draw(st.sampled_from(list(InvalidCandleReason)))

    if reason == InvalidCandleReason.INVALID_TIMESTAMP:
        timestamp = draw(st.one_of(
            st.just("not-a-date"),
            st.just(""),
            st.just("99999-99-99"),
            st.integers().map(str),
        ))
        return Candle(
            source=base.source, symbol=base.symbol, timestamp=timestamp,
            open=price, high=high, low=low, close=price, volume=0.0,
        )

    if reason == InvalidCandleReason.NEGATIVE_VOLUME:
        volume = draw(st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False))
        return Candle(
            source=base.source, symbol=base.symbol, timestamp=base.timestamp,
            open=price, high=high, low=low, close=price, volume=volume,
        )

    if reason == InvalidCandleReason.LOW_GREATER_THAN_HIGH:
        return Candle(
            source=base.source, symbol=base.symbol, timestamp=base.timestamp,
            open=price, high=low, low=high, close=price, volume=0.0,
        )

    if reason == InvalidCandleReason.OPEN_OUTSIDE_RANGE:
        open_ = draw(st.one_of(
            st.floats(max_value=low - 0.01, allow_nan=False, allow_infinity=False),
            st.floats(min_value=high + 0.01, allow_nan=False, allow_infinity=False),
        ))
        return Candle(
            source=base.source, symbol=base.symbol, timestamp=base.timestamp,
            open=open_, high=high, low=low, close=price, volume=0.0,
        )

    if reason == InvalidCandleReason.CLOSE_OUTSIDE_RANGE:
        close = draw(st.one_of(
            st.floats(max_value=low - 0.01, allow_nan=False, allow_infinity=False),
            st.floats(min_value=high + 0.01, allow_nan=False, allow_infinity=False),
        ))
        return Candle(
            source=base.source, symbol=base.symbol, timestamp=base.timestamp,
            open=price, high=high, low=low, close=close, volume=0.0,
        )

def candles_strategy(min_size=5, max_size=50) -> SearchStrategy[Sequence[Candle]]:
    return st.lists(
        candle_strategy(),
        min_size=min_size,
        max_size=max_size,
        unique=True
    )

def invalid_candles_strategy(min_size=1, max_size=1, reason: InvalidCandleReason | None = None) -> SearchStrategy[Sequence[Candle]]:
    return st.lists(
        invalid_candle_strategy(reason=reason),
        min_size=min_size,
        max_size=max_size,
        unique=True
    )