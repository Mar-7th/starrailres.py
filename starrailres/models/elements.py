from typing import Dict

from msgspec import Struct


class ElementType(Struct):
    id: str  # element id
    name: str  # element name
    desc: str  # element description
    color: str  # element color
    icon: str  # element icon path


ElementIndex = Dict[str, ElementType]
