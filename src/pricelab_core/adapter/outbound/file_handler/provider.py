from pricelab_core.adapter.outbound.file_handler.factory import FileHandlerFactory
from pricelab_core.adapter.outbound.file_handler.strategy import FileHandlerStrategy


class FileHandlerProvider:
    def __init__(self, strategy: FileHandlerStrategy) -> None:
        self._strategy = strategy

    def __call__(self, file_path: str) -> FileHandlerFactory:
        return FileHandlerFactory(file_path, self._strategy)