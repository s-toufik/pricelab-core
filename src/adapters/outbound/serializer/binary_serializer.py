import msgpack
from typing import TypeVar, Type
from dataclasses import asdict

from application.ports.outbound.serializer import Serializer

T = TypeVar("T")
class BinarySerializer(Serializer):

    def serialize(inputs: T) -> bytes:
        return msgpack.packb(asdict(inputs))

    def deserialize(inputs: bytes, cls: Type[T]) -> T:
        return cls(**msgpack.unpackb(inputs, raw=False))