from typing import List, Optional

from msgspec import Struct


class LevelInfo(Struct):
    id: str
    level: int = 0


class AvatarInfo(Struct):
    id: str
    name: str
    icon: str


class PathInfo(Struct):
    id: str
    name: str
    icon: str


class ElementInfo(Struct):
    id: str
    name: str
    color: str
    icon: str


class SkillInfo(Struct):
    id: str
    name: str
    level: int
    max_level: int
    element: Optional[ElementInfo]
    type: str
    type_text: str
    effect: str
    effect_text: str
    simple_desc: str
    desc: str
    icon: str


class SkillTreeInfo(Struct):
    id: str
    level: int
    icon: str


class PropertyInfo(Struct):
    type: str
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool


class AttributeInfo(Struct):
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool


class SubAffixInfo(Struct):
    id: str
    cnt: int
    step: int = 0


class RelicBasicInfo(Struct):
    id: str
    level: int = 1
    main_affix_id: Optional[str] = None
    sub_affix_info: List[SubAffixInfo] = []


class LightConeBasicInfo(Struct):
    id: str
    rank: int = 1
    level: int = 1
    promotion: int = 0


class CharacterBasicInfo(Struct):
    id: str
    rank: int = 0
    level: int = 1
    promotion: int = 0
    skill_tree_levels: List[LevelInfo] = []
    light_cone: Optional[LightConeBasicInfo] = None
    relics: Optional[List[RelicBasicInfo]] = None


class RelicInfo(Struct):
    id: str
    name: str
    set_id: str
    set_name: str
    rarity: int
    level: int
    icon: str
    main_affix: Optional[PropertyInfo] = None
    sub_affix: List[PropertyInfo] = []


class RelicSetInfo(Struct):
    id: str
    name: str
    icon: str
    num: int
    desc: str = ""
    properties: List[PropertyInfo] = []


class LightConeInfo(Struct):
    id: str
    name: str
    rarity: int
    rank: int
    level: int
    promotion: int
    icon: str
    preview: str
    portrait: str
    path: Optional[PathInfo] = None
    attributes: List[AttributeInfo] = []
    properties: List[PropertyInfo] = []


class CharacterInfo(Struct):
    id: str
    name: str
    rarity: int
    rank: int
    level: int
    promotion: int
    icon: str
    preview: str
    portrait: str
    rank_icons: List[str] = []
    path: Optional[PathInfo] = None
    element: Optional[ElementInfo] = None
    skills: List[SkillInfo] = []
    skill_trees: List[SkillTreeInfo] = []
    light_cone: Optional[LightConeInfo] = None
    relics: List[RelicInfo] = []
    relic_sets: List[RelicSetInfo] = []
    attributes: List[AttributeInfo] = []
    additions: List[AttributeInfo] = []
    properties: List[PropertyInfo] = []
