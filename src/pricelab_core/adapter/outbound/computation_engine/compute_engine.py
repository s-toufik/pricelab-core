from typing import Any, Sequence

from pricelab_core.adapter.outbound.logger.logger_instance import logger


class ComputeEngine:
    def __init__(self, engines: Sequence[Any]):
        self._engines = engines
        self._logger = logger

    def __getattr__(self, name: str) -> Any:
        for engine in self._engines:
            if hasattr(engine, name):
                return getattr(engine, name)

        self._logger.exception(f"{name} not found in {self._engines}")
        raise AttributeError
