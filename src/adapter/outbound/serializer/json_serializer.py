import json
from dataclasses import asdict
from typing import TypeVar, Type

from src.application.port.outbound.serializer.serializer import Serializer

T = TypeVar("T")


class JSONSerializer(Serializer):

    @staticmethod
    def serialize(inputs: T) -> str:
        return json.dumps(asdict(inputs))

    @staticmethod
    def deserialize(inputs: str, cls: Type[T]) -> T:
        return cls(**json.loads(inputs))
