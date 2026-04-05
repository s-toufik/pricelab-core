from typing import Sequence


from hypothesis import given

from pricelab_core.domain.model.candles.candle import Candle
from pricelab_core.domain.service.candles.candle_validator import CandleValidator
from tests.domain.models.candles_generator import candles_strategy, invalid_candles_strategy, InvalidCandleReason


class TestCandleValidator():

    @given(candles=candles_strategy())
    def test_valid_candles_validator(self, candles: Sequence[Candle]) -> None:
        for candle in candles:
            assert CandleValidator().status(candle)

    @given(candles=invalid_candles_strategy(min_size=1, max_size=10, reason=InvalidCandleReason.NEGATIVE_VOLUME))
    def test_invalid_candles_validator(self, candles: Sequence[Candle]) -> None:
        for invalid_candle in candles:
            assert CandleValidator().status(invalid_candle).is_valid is False
