from dataclasses import asdict
from typing import TypeVar, Type

from pricelab_core.application.port.outbound.serializer.serializer import Serializer

T = TypeVar("T")


class DictionarySerializer(Serializer):

    @staticmethod
    def serialize(inputs: T) -> dict:
        return asdict(inputs)

    @staticmethod
    def deserialize(inputs: dict, cls: Type[T]) -> T:
        return cls(**inputs)
