import datetime

from domain.models.candles.candle import Candle


class CandleValidator:

    def is_valid(self, candle: Candle) -> bool:
        return self._is_timestamp_valid(candle)

    @staticmethod
    def _is_timestamp_valid(candle: Candle) -> bool:
        if not isinstance(candle.timestamp, str):
            TypeError("Timestamp must be a string")
            return False
        try:
            datetime.datetime.fromisoformat(candle.timestamp)
            return True
        except ValueError:
            ValueError("Timestamp must be a string")
            return False