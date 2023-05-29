from typing import Dict

from msgspec import Struct


class DescriptionType(Struct):
    id: str  # description id
    title: str  # description title
    desc: str  # description desc


DescriptionIndex = Dict[str, DescriptionType]
