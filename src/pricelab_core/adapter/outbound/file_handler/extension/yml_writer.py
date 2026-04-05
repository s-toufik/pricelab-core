from typing import Dict, Any

import yaml

from pricelab_core.application.port.outbound.file_handler.writer import Writer


class YmlFileWriter(Writer):

    @staticmethod
    def write(file_path: str, data: Dict[str, Any]) -> None:
        with open(file_path, "w") as file:
            yaml.dump(data, file)