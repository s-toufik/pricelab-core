import datetime

from pricelab_core.domain.dto.validation_status import ValidationStatus
from pricelab_core.domain.model.candles.candle import Candle


class CandleValidator:

    def status(self, candle: Candle) -> ValidationStatus:

        if not (result := self._is_price_relation_valid(candle)).is_valid:
            return result

        if not (result := self._is_timestamp_valid(candle)).is_valid:
            return result

        return ValidationStatus.ok()

    @staticmethod
    def _is_timestamp_valid(candle: Candle) -> ValidationStatus:
        if not isinstance(candle.timestamp, str):
            return ValidationStatus.fail("Timestamp must be a string", TypeError)

        try:
            datetime.datetime.fromisoformat(candle.timestamp)
        except ValueError:
            return ValidationStatus.fail("Timestamp must be ISO format", ValueError)

        return ValidationStatus.ok()

    @staticmethod
    def _is_price_relation_valid(candle: Candle) -> ValidationStatus:
        if candle.volume < 0:
            return ValidationStatus.fail("Volume cannot be negative", ValueError)

        if candle.low > candle.high:
            return ValidationStatus.fail("Low cannot be greater than High", ValueError)

        if not (candle.low <= candle.open <= candle.high):
            return ValidationStatus.fail("Open must be within [low, high]", ValueError)

        if not (candle.low <= candle.close <= candle.high):
            return ValidationStatus.fail("Close must be within [low, high]", ValueError)

        return ValidationStatus.ok()
