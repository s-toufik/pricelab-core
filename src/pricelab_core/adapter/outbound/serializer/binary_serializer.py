from dataclasses import asdict
from typing import TypeVar, Type

import msgpack
from src.pricelab_core.application.port.outbound.serializer.serializer import Serializer

T = TypeVar("T")


class BinarySerializer(Serializer):

    @staticmethod
    def serialize(inputs: T) -> bytes:
        return msgpack.packb(asdict(inputs))

    @staticmethod
    def deserialize(inputs: bytes, cls: Type[T]) -> T:
        return cls(**msgpack.unpackb(inputs, raw=False))
