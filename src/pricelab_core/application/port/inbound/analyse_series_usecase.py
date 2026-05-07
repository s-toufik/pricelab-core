from typing import Sequence, TypeVar, Protocol

from pricelab_core.domain.model.analytics.analytics import Analytics

T = TypeVar("T")


class AnalyseSeriesUseCase(Protocol[T]):
    def execute(self, sequence: Sequence[T], params: dict) -> Sequence[Analytics]: ...
