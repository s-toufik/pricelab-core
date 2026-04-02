from typing import Any, Sequence

from src.adapter.outbound.logger.loguru_logger import LoguruLogger


class ComputeEngine:
    def __init__(self, engines: Sequence[Any]):
        self._engines = engines
        self._logger = LoguruLogger()

    def __getattr__(self, name: str) -> Any:
        for engine in self._engines:
            if hasattr(engine, name):
                return getattr(engine, name)

        self._logger.exception(f"{name} not found in {self._engines}")
        raise AttributeError
