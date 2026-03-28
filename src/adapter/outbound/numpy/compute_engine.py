from typing import Sequence

import numpy as np
from numpy import ndarray

from port.outbound.series_computation import SeriesComputation

class ComputeEngine(SeriesComputation):

    def field(self, sequence: Sequence[float]) -> np.ndarray:
        return np.array(sequence)

    def returns(self, sequence: Sequence[float]) -> np.ndarray:

        if len(sequence) < 2:
            return self._empty_array()

        array = self._convert_sequence_to_array(sequence)

        ratio = array[1:] / array[:-1]
        ratio = np.where(ratio <= 0, np.nan, ratio)
        return np.log(ratio)


    def rolling_average(self, sequence: Sequence[float], window: int = 5) -> np.ndarray:
        if len(sequence) < window:
            return self._empty_array()
        array = self._convert_sequence_to_array(sequence)
        return np.convolve(array, np.ones(window) / window, mode="valid")

    def rolling_standard_deviation(self, sequence: Sequence[float], window: int = 5) -> np.ndarray:
        if len(sequence) < window:
            return self._empty_array()
        array = self._convert_sequence_to_array(sequence)
        return np.array([
            np.std(array[i:i + window])
            for i in range(len(array) - window + 1)
        ])

    @staticmethod
    def _empty_array() -> ndarray:
        return np.array([], dtype=np.float64)

    @staticmethod
    def _convert_sequence_to_array(sequence: Sequence[float]) -> ndarray:
        if not isinstance(sequence, np.ndarray):
            array = np.asarray(sequence, dtype=np.float64)
        else:
            array = sequence
        return array
