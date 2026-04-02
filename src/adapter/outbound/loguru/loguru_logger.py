import threading

from application.port.outbound.logger_interface import LoggerInterface
from loguru import logger as loguru_logger

class LoguruLogger(LoggerInterface):

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.__init__logger()

        return cls._instance

    def __init__logger(self):
        self._logger = loguru_logger

    def info(self, msg: str, **kwargs):
        self._logger.opt(depth=1).info(msg)

    def warning(self, msg: str, **kwargs) -> None:
        self._logger.opt(depth=1).warning(msg)

    def error(self, msg: str, **kwargs) -> None:
        self._logger.opt(depth=1).error(msg)

    def critical(self, msg: str, **kwargs) -> None:
        self._logger.opt(depth=1).critical(msg)

    def debug(self, msg: str, **kwargs) -> None:
        self._logger.opt(depth=1).debug(msg)

    def exception(self, msg: str, **kwargs) -> None:
        self._logger.opt(depth=1).exception(msg)