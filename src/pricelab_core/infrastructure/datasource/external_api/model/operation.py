from dataclasses import dataclass

from pricelab_core.infrastructure.http.enum.http_method import HttpMethod
from .source import ApiSource
from ...enum.data_source_type import DataSourceType


@dataclass(slots=True)
class ApiOperation:
    name: str
    source: ApiSource
    type: DataSourceType
    path: str
    method: HttpMethod
