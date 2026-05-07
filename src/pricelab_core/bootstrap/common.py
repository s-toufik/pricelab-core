from pricelab_core.adapter.outbound.computation_engine.compute_engine import ComputeEngine
from pricelab_core.adapter.outbound.computation_engine.numpy_arithmetic_operation import (
    NumPyArithmeticOperation,
)
from pricelab_core.adapter.outbound.computation_engine.scipy_calculus_operation import (
    ScipyCalculusOperation,
)
from pricelab_core.adapter.outbound.logger.loguru_logger import LoguruLogger
from pricelab_core.application.port.outbound.computation_engine.engine import Engine
from pricelab_core.application.port.outbound.logger.logger import Logger


compute_engine: Engine = ComputeEngine(NumPyArithmeticOperation(), ScipyCalculusOperation())

logger: Logger = LoguruLogger()
