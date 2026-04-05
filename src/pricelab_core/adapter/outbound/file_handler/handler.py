from pricelab_core.adapter.outbound.file_handler.provider import FileHandlerProvider
from pricelab_core.adapter.outbound.file_handler.strategy import FileHandlerStrategy
from pricelab_core.adapter.outbound.file_handler.extension.yml_reader import YmlFileReader
from pricelab_core.adapter.outbound.file_handler.extension.yml_writer import YmlFileWriter

strategy = FileHandlerStrategy(
    {
        "yml": {
            "reader": YmlFileReader(),
            "writer": YmlFileWriter()
        },
    }
)

Handler = FileHandlerProvider(strategy)