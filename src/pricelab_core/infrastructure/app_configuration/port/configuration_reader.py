from typing import Protocol

from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration


class ConfigurationReader(Protocol):
    def read(self) -> AppConfiguration: ...
