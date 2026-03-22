from dataclasses import is_dataclass
from typing import Type, TypeVar, ClassVar
import struct

T = TypeVar("T")

class BinarySerializer:

    _STRUCT: ClassVar[struct.Struct]
    _FIELD_INFO: ClassVar[list]

    @classmethod
    def to_bytes(cls, obj: T) -> bytes:
        if not is_dataclass(obj):
            raise TypeError("to_bytes expects a dataclass instance")

        values = []
        for name, typ, size in cls._FIELD_INFO:
            value = getattr(obj, name)
            if typ == str:
                encoded = value.encode("utf-8")
                padded = encoded.ljust(size, b"\0")
                values.append(padded)
            else:
                values.append(value)

        return cls._STRUCT.pack(*values)

    @classmethod
    def from_bytes(cls, data: bytes) -> T:
        unpacked = cls._STRUCT.unpack(data)
        kwargs = {}
        for (name, typ, size), value in zip(cls._FIELD_INFO, unpacked):
            if typ == str:
                kwargs[name] = value.rstrip(b"\0").decode("utf-8")
            else:
                kwargs[name] = value
        return cls._DATACLASS(**kwargs)

    @classmethod
    def setup(cls, dataclass_type: Type[T], field_info: list[tuple[str, type, int]]):
        cls._DATACLASS = dataclass_type
        cls._FIELD_INFO = field_info

        fmt = ">"
        for _, typ, size in field_info:
            if typ == str:
                fmt += f"{size}s"
            elif typ == float:
                fmt += "d"
            elif typ == int:
                fmt += "q"
            else:
                raise TypeError(f"Unsupported field type: {typ}")

        cls._STRUCT = struct.Struct(fmt)