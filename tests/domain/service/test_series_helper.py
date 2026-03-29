from datetime import timezone

from hypothesis import strategies as st
from hypothesis.strategies import SearchStrategy
from hypothesis import given

from domain.model.candle import Candle
from domain.service.prediction_series import PredictionSeries
from domain.service.quote_series import QuoteSeries
from src.domain.model.quote import Quote
from domain.model.prediction import Prediction
from domain.model.computed_indicators import ComputedIndicators
from domain.service.candle_series import CandleSeries


# -----------------------------
# Helpers
# -----------------------------
def iso_datetime_strategy() -> SearchStrategy[str]:
    """ISO 8601 timestamp generator"""
    return (
        st.datetimes(timezones=st.just(timezone.utc))
        .map(lambda dt: dt.replace(microsecond=0).isoformat())
    )


def safe_float(min_v: float, max_v: float) -> SearchStrategy[float]:
    """Safe float avoiding NaN/inf"""
    return st.floats(min_value=min_v, max_value=max_v, allow_nan=False, allow_infinity=False)


# -----------------------------
# Candle strategy
# -----------------------------
@st.composite
def build_candle(draw) -> Candle:
    low = draw(safe_float(0, 100))
    high = draw(safe_float(low, low + 100))
    open_ = draw(safe_float(low, high))
    close = draw(safe_float(low, high))

    return Candle(
        source=draw(st.sampled_from(["binance", "coinbase", "kraken"])),
        symbol=draw(st.sampled_from(["BTCUSDT", "ETHUSDT", "SOLUSDT"])),
        timestamp=draw(iso_datetime_strategy()),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=draw(safe_float(0, 1e6))
    )


def build_candle_series() -> SearchStrategy[CandleSeries]:
    return st.lists(
        build_candle(),
        min_size=1,
        max_size=10
    ).map(lambda candles: CandleSeries(candles))


# -----------------------------
# Quote strategy
# -----------------------------
@st.composite
def build_quote(draw) -> Quote:
    bid_val = draw(safe_float(0, 1000))
    ask_val = draw(safe_float(bid_val, bid_val + 10))
    last_val = draw(safe_float(bid_val, ask_val))

    return Quote(
        source=draw(st.sampled_from(["binance", "coinbase", "kraken"])),
        symbol=draw(st.sampled_from(["BTCUSDT", "ETHUSDT", "SOLUSDT"])),
        timestamp=draw(iso_datetime_strategy()),
        bid=bid_val,
        ask=ask_val,
        last=last_val,
        volume=draw(safe_float(0, 1e6))
    )

def build_quote_series() -> SearchStrategy[QuoteSeries]:
    return st.lists(
        build_quote(),
        min_size=1,
        max_size=10
    ).map(lambda quote: QuoteSeries(quote))

# -----------------------------
# Prediction strategy
# -----------------------------
@st.composite
def build_prediction(draw) -> Prediction:
    predicted_price = draw(safe_float(0, 10000))
    confidence = draw(st.floats(min_value=0, max_value=1))
    horizon = draw(st.integers(min_value=1, max_value=365))  # horizon in days

    return Prediction(
        source=draw(st.sampled_from(["model_a", "model_b"])),
        symbol=draw(st.sampled_from(["BTCUSDT", "ETHUSDT"])),
        timestamp=draw(iso_datetime_strategy()),
        predicted_price=predicted_price,
        confidence=confidence,
        horizon=horizon
    )

def build_prediction_series() -> SearchStrategy[PredictionSeries]:
    return st.lists(
        build_prediction(),
        min_size=1,
        max_size=10
    ).map(lambda prediction: PredictionSeries(prediction))


# -----------------------------
# ComputedIndicators strategy
# -----------------------------
@st.composite
def build_computed_indicators(draw, min_len: int = 1, max_len: int = 50) -> ComputedIndicators:
    length = draw(st.integers(min_value=min_len, max_value=max_len))
    times = draw(st.lists(iso_datetime_strategy(), min_size=length, max_size=length))
    field = draw(st.lists(safe_float(0, 1000), min_size=length, max_size=length))
    returns = draw(st.lists(safe_float(-1, 1), min_size=length, max_size=length))
    rolling_avg = draw(st.lists(safe_float(0, 1000), min_size=length, max_size=length))
    rolling_std = draw(st.lists(safe_float(0, 100), min_size=length, max_size=length))

    return ComputedIndicators(
        time=times,
        field=field,
        returns=returns,
        rolling_average=rolling_avg,
        rolling_standard_deviation=rolling_std
    )


@given(ci=build_computed_indicators())
def test_computed_indicators_lengths(ci: ComputedIndicators):
    n = len(ci.time)
    assert n == len(ci.field) == len(ci.returns) == len(ci.rolling_average) == len(ci.rolling_standard_deviation)