from typing import Dict, Optional

from msgspec import Struct


class PropertyType(Struct):
    type: str  # property type
    name: str  # property name
    field: str  # property field for affix
    affix: bool  # is relic or light cone affix
    ratio: bool  # is added ratio
    percent: bool  # is percent
    order: int  # property order
    icon: Optional[str]  # property icon path


PropertyIndex = Dict[str, PropertyType]
