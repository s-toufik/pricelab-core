from dataclasses import dataclass
from typing import Dict, Union

from pricelab_core.infrastructure.datasource.external_api.model.operation import ApiOperation
from pricelab_core.infrastructure.datasource.repository.operation import FileOperation

Operation = Union[FileOperation, ApiOperation]


@dataclass(slots=True)
class UseCase:
    name: str
    operation: Operation
    parameters: Dict[str, str]
