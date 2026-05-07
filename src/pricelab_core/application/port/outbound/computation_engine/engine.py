from typing import Protocol

from pricelab_core.application.port.outbound.computation_engine.arithmetic_operation import (
    ArithmeticOperation,
)
from pricelab_core.application.port.outbound.computation_engine.calculus_operation import (
    CalculusOperation,
)


class Engine(Protocol):
    @property
    def arithmetic(self) -> ArithmeticOperation: ...

    @property
    def calculus(self) -> CalculusOperation: ...
