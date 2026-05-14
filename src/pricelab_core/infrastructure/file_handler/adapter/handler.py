from pricelab_core.infrastructure.file_handler.adapter.provider import FileHandlerProvider
from pricelab_core.infrastructure.file_handler.adapter.strategy import FileHandlerStrategy
from pricelab_core.infrastructure.file_handler.adapter.extension.yml_reader import YmlFileReader
from pricelab_core.infrastructure.file_handler.adapter.extension.yml_writer import YmlFileWriter

strategy = FileHandlerStrategy(
    {
        "yml": {"reader": YmlFileReader(), "writer": YmlFileWriter()},
    }
)

Handler = FileHandlerProvider(strategy)
