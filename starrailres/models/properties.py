from typing import Dict

from msgspec import Struct


class PropertyType(Struct):
    type: str  # property type
    name: str  # property name
    field: str  # property field for affix
    affix: bool  # is relic or light cone affix
    ratio: bool  # is added ratio
    order: int  # property order
    icon: str  # property icon path


PropertyIndex = Dict[str, PropertyType]
