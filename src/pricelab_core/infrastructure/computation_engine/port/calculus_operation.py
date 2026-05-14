from typing import Sequence, Protocol

from pricelab_core.domain.base.const_typing import Numeric, Kind


class CalculusOperation(Protocol):
    def integrate(self, sequence: Sequence[Numeric], dx: float) -> float: ...

    def interpolate(
        self, sequence: Sequence[Numeric], kind: Kind = "linear"
    ) -> Sequence[Numeric]: ...
