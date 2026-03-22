from abc import ABC, abstractmethod
from typing import TypeVar, Type

T = TypeVar("T")
class Serializer(ABC):

    @staticmethod
    @abstractmethod
    def serialize(inputs: T) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def deserialize(inputs: bytes, cls: Type[T]) -> T:
        pass