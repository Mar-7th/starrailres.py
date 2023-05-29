from typing import Dict, List, Literal

from msgspec import Struct

from .common import Property


class RelicType(Struct):
    id: str
    set_id: str
    name: str
    rarity: int
    type: Literal["HEAD", "HAND", "BODY", "FOOT", "NECK", "OBJECT"]
    max_level: int
    main_affix_id: str
    sub_affix_id: str
    icon: str


class RelicSetType(Struct):
    id: str
    name: str
    properties: List[List[Property]]
    icon: str
    guide_overview: List[str]


class AffixType(Struct):
    affix_id: str
    property: str
    base: float
    step: float
    step_num: int = 0


class RelicMainAffixType(Struct):
    id: str
    affixs: Dict[str, AffixType]


class RelicSubAffixType(Struct):
    id: str
    affixs: Dict[str, AffixType]


RelicIndex = Dict[str, RelicType]
RelicSetIndex = Dict[str, RelicSetType]
RelicMainAffixIndex = Dict[str, RelicMainAffixType]
RelicSubAffixIndex = Dict[str, RelicSubAffixType]
