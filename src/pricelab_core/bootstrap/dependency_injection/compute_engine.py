from pricelab_core.infrastructure.computation_engine.adapter.compute_engine import ComputeEngine
from pricelab_core.infrastructure.computation_engine.adapter.numpy_arithmetic_operation import (
    NumPyArithmeticOperation,
)
from pricelab_core.infrastructure.computation_engine.adapter.scipy_calculus_operation import (
    ScipyCalculusOperation,
)
from pricelab_core.infrastructure.computation_engine.port.engine import Engine

compute_engine: Engine = ComputeEngine(NumPyArithmeticOperation(), ScipyCalculusOperation())
