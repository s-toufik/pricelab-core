from typing import Dict, List, Union
from dataclasses import dataclass

from pricelab_core.infrastructure.app_configuration.enum.run_type_application import (
    RunTypeApplication,
)
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)
from pricelab_core.infrastructure.datasource.data_use_case.use_case import UseCase
from pricelab_core.infrastructure.datasource.enum.data_source_type import DataSourceType
from pricelab_core.infrastructure.datasource.external_api.model.source import ApiSource
from pricelab_core.infrastructure.datasource.repository.file_source import FileSource

DataSourceBaseType = Union[ApiSource, FileSource]


@dataclass(frozen=True, slots=True)
class AppConfiguration:
    env: RunTypeEnvironment
    run: RunTypeApplication
    data_source: Dict[DataSourceType, Dict[str, DataSourceBaseType]]
    use_case: Dict[str, List[UseCase]]
    telemetry: Dict[str, str]
