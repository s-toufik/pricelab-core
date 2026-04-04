import threading

from src.adapter.outbound.computation_engine.compute_engine import ComputeEngine
from src.adapter.outbound.computation_engine.numpy_arithmetic_engine import NumPyArithmeticEngine
from src.adapter.outbound.computation_engine.scipy_scientific_engine import ScipyScientificEngine


class StartComputeEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._start_engine()
        return cls._instance

    def _start_engine(self):
        self._engine = ComputeEngine(
            (NumPyArithmeticEngine(),
            ScipyScientificEngine())
        )

    @property
    def engine(self):
        return self._engine
