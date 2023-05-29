from typing import Dict

from msgspec import Struct


class PathType(Struct):
    id: str  # path id
    text: str  # path text
    name: str  # path name
    desc: str  # path description
    icon: str  # path icon path


PathIndex = Dict[str, PathType]
