from msgspec import Struct


class Quantity(Struct):
    id: str
    num: int


class Property(Struct):
    type: str
    value: float


class Promotion(Struct):
    base: float
    step: float
