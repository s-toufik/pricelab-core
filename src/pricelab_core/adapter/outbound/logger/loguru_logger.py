import threading

from loguru import logger as loguru_logger

from pricelab_core.application.port.outbound.logger.logger_interface import LoggerInterface


class LoguruLogger(LoggerInterface):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__init__logger()

        return cls._instance

    def __init__logger(self):
        self._logger = loguru_logger

    def info(self, msg: str):
        self._logger.opt(depth=1).info(msg)

    def warning(self, msg: str) -> None:
        self._logger.opt(depth=1).warning(msg)

    def error(self, msg: str) -> None:
        self._logger.opt(depth=1).error(msg)

    def critical(self, msg: str) -> None:
        self._logger.opt(depth=1).critical(msg)

    def debug(self, msg: str) -> None:
        self._logger.opt(depth=1).debug(msg)

    def exception(self, msg: str) -> None:
        self._logger.opt(depth=1).exception(msg)
