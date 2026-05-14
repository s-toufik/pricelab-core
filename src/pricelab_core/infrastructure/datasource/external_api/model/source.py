from dataclasses import dataclass

from pricelab_core.infrastructure.datasource.base import DataSourceBase


@dataclass(slots=True)
class ApiSource(DataSourceBase):
    base_url: str
    timeout: int
    retry: int
