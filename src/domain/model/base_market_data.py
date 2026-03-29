import datetime
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BaseMarketData:
    source: str
    symbol: str
    timestamp: str

    def __post_init__(self):
        self._validate_timestamp()

    def _validate_timestamp(self):
        if not isinstance(self.timestamp, str):
            raise TypeError("Timestamp must be a string")
        try:
            datetime.datetime.fromisoformat(self.timestamp)
        except:
            raise ValueError