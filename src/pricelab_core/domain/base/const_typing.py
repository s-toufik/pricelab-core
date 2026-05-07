import numbers
from typing import TypeVar, Union, Literal

Numeric = TypeVar("Numeric", bound=numbers.Real)
Kind = Union[
    Literal[
        "linear",
        "nearest",
        "nearest-up",
        "zero",
        "slinear",
        "quadratic",
        "cubic",
        "previous",
        "next",
    ],
    int,
]
