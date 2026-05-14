from dataclasses import dataclass
from enum import Enum

from pricelab_core.infrastructure.datasource.enum.data_source_type import DataSourceType
from pricelab_core.infrastructure.datasource.repository.file_source import FileSource


class Action(Enum):
    read = "read"
    write = "write"
    delete = "delete"


@dataclass(slots=True)
class FileOperation:
    name: str
    source: FileSource
    type: DataSourceType
    action: Action
