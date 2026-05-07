from pricelab_core.application.port.outbound.computation_engine.arithmetic_operation import (
    ArithmeticOperation,
)
from pricelab_core.application.port.outbound.computation_engine.calculus_operation import (
    CalculusOperation,
)


class ComputeEngine:
    def __init__(self, arithmetic: ArithmeticOperation, calculus: CalculusOperation):
        self._arithmetic = arithmetic
        self._calculus = calculus

    @property
    def arithmetic(self) -> ArithmeticOperation:
        return self._arithmetic

    @property
    def calculus(self) -> CalculusOperation:
        return self._calculus
