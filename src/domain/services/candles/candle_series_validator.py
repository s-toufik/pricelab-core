from dataclasses import fields
from typing import Sequence

from domain.models.candles.candle_series import CandleSeries


class CandleSeriesValidator:

    def is_valid_for_analysis(self, sequence: CandleSeries) -> bool:
        return self._is_sequence_field_length_valid(sequence)

    @staticmethod
    def _is_sequence_field_length_valid(sequence: CandleSeries) -> bool:
        lengths = {
            field.name: len(getattr(sequence, field.name))
            for field in fields(CandleSeries)
            if isinstance(getattr(sequence, field.name), Sequence)
               and not isinstance(getattr(sequence, field.name), str)
        }

        if len(set(lengths.values())) != 1:
            ValueError(
                f"All sequences must have the same length, got: {lengths}"
            )
            return False

        return True
