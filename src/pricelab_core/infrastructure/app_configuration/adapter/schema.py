from pydantic import BaseModel
from typing import Dict, Sequence

from pricelab_core.infrastructure.app_configuration.enum.connector_type import ConnectorType
from pricelab_core.infrastructure.app_configuration.enum.run_type_application import (
    RunTypeApplication,
)
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)
from pricelab_core.infrastructure.app_configuration.model.configuration import AppConfiguration
from pricelab_core.infrastructure.app_configuration.model.connector import ConnectorTyping

from pricelab_core.infrastructure.app_configuration.model.cronjob import CronJob
from pricelab_core.infrastructure.app_configuration.model.operation import OperationTyping


class AppConfigurationSchema(BaseModel):
    env: RunTypeEnvironment
    run: RunTypeApplication
    connector: Dict[ConnectorType, Dict[str, ConnectorTyping]]
    operation: Dict[str, OperationTyping]
    cronjob: Sequence[CronJob]


class MapperDomainSchema:
    @staticmethod
    def map(app_configuration_schema: AppConfigurationSchema) -> AppConfiguration:
        return AppConfiguration(**vars(app_configuration_schema))
