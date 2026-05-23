from dataclasses import dataclass
from typing import Dict, Union

from pricelab_core.infrastructure.app_configuration.enum.connector_type import ConnectorType
from pricelab_core.infrastructure.authentication import AuthTyping


@dataclass(slots=True)
class BaseConnector:
    name: str
    type: ConnectorType
    auth: AuthTyping


@dataclass(slots=True)
class ApiConnector(BaseConnector):
    base_url: str
    timeout: int
    retry: int


@dataclass(slots=True)
class DatabaseConnector(BaseConnector):
    engine: str
    host: str
    port: int
    default_name: str
    pool: Dict[str, int]


@dataclass(slots=True)
class FileConnector(BaseConnector):
    base_path: str


@dataclass(slots=True)
class TelemetryConnector(BaseConnector):
    host: str
    port: int


ConnectorTyping = Union[ApiConnector, FileConnector, DatabaseConnector, TelemetryConnector]
