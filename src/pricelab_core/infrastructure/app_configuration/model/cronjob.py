from dataclasses import dataclass

from pricelab_core.infrastructure.app_configuration.model.operation import OperationTyping


@dataclass(slots=True)
class CronJob:
    name: str
    cron: str
    operation: OperationTyping
