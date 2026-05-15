from typing import Dict
from dataclasses import dataclass
from pricelab_core.infrastructure.datasource.base import DataSourceBase


@dataclass(slots=True)
class DatabaseSource(DataSourceBase):
    engine: str
    host: str
    port: int
    default_name: str
    pool: Dict[str, int]
