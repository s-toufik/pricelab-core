from typing import Protocol

from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration


class Configuration(Protocol):
    def load(self) -> AppConfiguration | None: ...

    def reload(self) -> AppConfiguration | None: ...
