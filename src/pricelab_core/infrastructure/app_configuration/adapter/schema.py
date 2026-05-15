from pydantic import BaseModel
from typing import Dict, List

from pricelab_core.infrastructure.app_configuration.enum.run_type_application import (
    RunTypeApplication,
)
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)
from pricelab_core.infrastructure.app_configuration.model.configuration import (
    DataSourceBaseType,
    AppConfiguration,
)
from pricelab_core.infrastructure.datasource.data_use_case.use_case import UseCase
from pricelab_core.infrastructure.datasource.enum.data_source_type import DataSourceType


class AppConfigurationSchema(BaseModel):
    env: RunTypeEnvironment
    run: RunTypeApplication
    datasource: Dict[DataSourceType, Dict[str, DataSourceBaseType]]
    use_case: Dict[str, List[UseCase]]
    telemetry: Dict[str, str]


class MapperDomainSchema:
    @staticmethod
    def map(app_configuration_schema: AppConfigurationSchema) -> AppConfiguration:
        return AppConfiguration(**vars(app_configuration_schema))
