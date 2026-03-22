from dataclasses import fields
from typing import Dict, Type, TypeVar, Union

T = TypeVar("T", bound="SerializableDataclass")
ValueType = Union[str, int, float]

class SerializableDataclass:
    def to_dict(self) -> Dict[str, ValueType]:
        return {field.name: getattr(self, field.name) for field in fields(self)}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, ValueType]) -> T:
        return cls(**data)