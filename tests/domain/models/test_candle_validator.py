import pytest
from jedi.inference.value.iterable import Sequence

from domain.model.candles.candle import Candle
from domain.service.candles.candle_validator import CandleValidator
from tests.domain.models.candles_generator import candles_strategy, invalid_candles_strategy, InvalidCandleReason


class TestCandleValidator():

    @pytest.fixture
    def valid_candles_creation(self) -> Sequence[Candle]:
        return candles_strategy().example()

    @staticmethod
    def invalid_candles_creation(reason: InvalidCandleReason) -> Sequence[Candle]:
        return invalid_candles_strategy(min_size=1, max_size=10, reason= reason).example()

    def test_valid_candles_validator(self, valid_candles_creation) -> None:
        for candle in valid_candles_creation:
            assert CandleValidator().status(candle)

    def test_invalid_candles_validator(self) -> None:
        candles = self.invalid_candles_creation(InvalidCandleReason.INVALID_TIMESTAMP)
        for invalid_candle in candles:
            assert CandleValidator().status(invalid_candle).is_valid is False