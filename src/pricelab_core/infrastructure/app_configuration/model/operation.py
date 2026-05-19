from dataclasses import dataclass
from typing import Dict, Union, List

from pricelab_core.infrastructure.app_configuration.enum.file_operation_action import (
    FileOperationAction,
)
from pricelab_core.infrastructure.app_configuration.model.connector import ConnectorTyping
from pricelab_core.infrastructure.http.enum.http_method import HttpMethod

ParamType = Union[str, List[str]]


@dataclass(slots=True)
class BaseOperation:
    name: str
    connector: ConnectorTyping


@dataclass(slots=True)
class ApiOperation(BaseOperation):
    endpoint: str
    method: HttpMethod
    parameters: Dict[str, ParamType]


@dataclass(slots=True)
class FileOperation(BaseOperation):
    action: FileOperationAction
    parameters: Dict[str, ParamType]


OperationTyping = Union[FileOperation, ApiOperation]
