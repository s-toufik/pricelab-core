import json
from dataclasses import asdict
from typing import TypeVar, Type

from src.port.outbound.serializer import Serializer

T = TypeVar("T")
class JSONSerializer(Serializer):

    def serialize(inputs: T) -> str:
        return json.dumps(asdict(inputs))

    def deserialize(inputs: str, cls : Type[T]) -> T:
        return cls(**json.loads(inputs))