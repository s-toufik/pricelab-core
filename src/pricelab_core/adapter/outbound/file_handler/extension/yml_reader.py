from typing import Dict, Any

import yaml

from pricelab_core.application.port.outbound.file_handler.reader import Reader


class YmlFileReader(Reader):

    @staticmethod
    def read(file_path: str) -> Dict[str, Any]:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)