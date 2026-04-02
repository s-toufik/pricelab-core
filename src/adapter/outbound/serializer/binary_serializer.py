from dataclasses import asdict
from typing import TypeVar, Type

import msgpack
from src.application.port.outbound.serializer.serializer import Serializer

T = TypeVar("T")


class BinarySerializer(Serializer):

    def serialize(inputs: T) -> bytes:
        return msgpack.packb(asdict(inputs))

    def deserialize(inputs: bytes, cls: Type[T]) -> T:
        return cls(**msgpack.unpackb(inputs, raw=False))
