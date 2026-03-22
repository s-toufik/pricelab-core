import math
from dataclasses import dataclass

from src.ports.outbound.dictionary_serializer import SerializableDataclass


@dataclass(frozen=True, slots=True)
class Prediction(SerializableDataclass):
    symbol: str
    predicted_price: float
    confidence: float
    horizon_ms: int
    timestamp: int

    def __post_init__(self):
        self._validate_symbol()
        self._validate_predicted_price()
        self._validate_confidence()
        self._validate_horizon()
        self._validate_timestamp()

    def _validate_symbol(self) -> None:
        if not self.symbol:
            raise ValueError("Symbol cannot be empty")

    def _validate_predicted_price(self) -> None:
        if not math.isfinite(self.predicted_price):
            raise ValueError("Predicted price must be finite")
        if self.predicted_price < 0:
            raise ValueError("Predicted price must be non-negative")

    def _validate_confidence(self) -> None:
        if not math.isfinite(self.confidence):
            raise ValueError("confidence must be finite")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")

    def _validate_horizon(self) -> None:
        if self.horizon_ms <= 0:
            raise ValueError("horizon_ms must be > 0")

    def _validate_timestamp(self) -> None:
        if self.timestamp < 0:
            raise ValueError("timestamp must be >= 0")