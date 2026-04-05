from typing import Dict, TypedDict

from pricelab_core.application.port.outbound.file_handler.reader import Reader
from pricelab_core.application.port.outbound.file_handler.writer import Writer

class FileHandlerDict(TypedDict):
    reader: Reader
    writer: Writer

class FileHandlerStrategy:

    def __init__(self, handlers: Dict[str, FileHandlerDict]) -> None:
        self._handlers = handlers

    def get_reader(self, extension: str) -> Reader:
        return self._handlers[extension]["reader"]

    def get_writer(self, extension: str) -> Writer:
        return self._handlers[extension]["writer"]

    def supports(self, extension: str) -> bool:
        return extension in self._handlers