from dataclasses import fields
from typing import Sequence

from src.domain.dto.validation_status import ValidationStatus
from src.domain.model.quotes.quote_series import QuoteSeries


class QuoteSeriesValidator:
    def is_valid_for_analysis(self, sequence: QuoteSeries) -> ValidationStatus:

        if not (result := self._is_sequence_field_length_valid(sequence)).is_valid:
            return result

        return ValidationStatus.ok()

    @staticmethod
    def _is_sequence_field_length_valid(sequence: QuoteSeries) -> ValidationStatus:
        lengths = {
            field.name: len(getattr(sequence, field.name))
            for field in fields(QuoteSeries)
            if isinstance(getattr(sequence, field.name), Sequence)
               and not isinstance(getattr(sequence, field.name), str)
        }

        values = lengths.values()
        if len(set(values)) != 1:
            return ValidationStatus.fail("All sequences must have the same length", ValueError)

        if all((v == 0 for v in values)):
            return ValidationStatus.fail("All numerical fields have zero size", ValueError)

        return ValidationStatus.ok()
