from dataclasses import dataclass

from pricelab_core.infrastructure.authentication.auth_type import Auth
from pricelab_core.infrastructure.datasource.enum.data_source_type import DataSourceType


@dataclass(slots=True)
class DataSourceBase:
    name: str
    type: DataSourceType
    auth: Auth
