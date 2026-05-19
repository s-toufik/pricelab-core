from typing import Dict, Sequence
from dataclasses import dataclass

from pricelab_core.infrastructure.app_configuration.enum.connector_type import ConnectorType
from pricelab_core.infrastructure.app_configuration.enum.run_type_application import (
    RunTypeApplication,
)
from pricelab_core.infrastructure.app_configuration.enum.run_type_environment import (
    RunTypeEnvironment,
)
from pricelab_core.infrastructure.app_configuration.model.connector import ConnectorTyping
from pricelab_core.infrastructure.app_configuration.model.cronjob import CronJob
from pricelab_core.infrastructure.app_configuration.model.operation import OperationTyping


@dataclass(frozen=True, slots=True)
class AppConfiguration:
    env: RunTypeEnvironment
    run: RunTypeApplication
    connector: Dict[ConnectorType, Dict[str, ConnectorTyping]]
    operation: Dict[str, OperationTyping]
    cronjob: Sequence[CronJob]
