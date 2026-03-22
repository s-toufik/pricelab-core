from dataclasses import asdict
from typing import TypeVar, Type

from src.ports.outbound.serializer import Serializer

T = TypeVar("T")
class DictionarySerializer(Serializer):

    def serialize(inputs: T) -> dict:
        return asdict(inputs)

    def deserialize(inputs: dict, cls: Type[T]) -> T:
        return cls(**inputs)