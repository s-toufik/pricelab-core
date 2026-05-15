from dataclasses import dataclass

from pricelab_core.infrastructure.datasource.base import DataSourceBase


@dataclass(slots=True)
class FileSource(DataSourceBase):
    engine: str
    base_path: str
