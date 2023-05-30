from typing import List, Optional

from msgspec import Struct


class BaseInfo(Struct):
    def to_dict(self):
        result = {}
        for field in self.__struct_fields__:
            value = getattr(self, field)
            if isinstance(value, BaseInfo):
                result[field] = value.to_dict()
            elif isinstance(value, list) and all(
                isinstance(i, BaseInfo) for i in value
            ):
                result[field] = [i.to_dict() for i in value]
            else:
                result[field] = value
        return result


class LevelInfo(BaseInfo):
    id: str
    level: int = 0


class PathInfo(BaseInfo):
    id: str
    name: str
    icon: str


class ElementInfo(BaseInfo):
    id: str
    name: str
    color: str
    icon: str


class SkillInfo(BaseInfo):
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


class PropertyInfo(BaseInfo):
    type: str
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool


class AttributeInfo(BaseInfo):
    field: str
    name: str
    icon: str
    value: float
    display: str
    percent: bool


class SubAffixInfo(BaseInfo):
    id: str
    cnt: int
    step: int = 0


class RelicBasicInfo(BaseInfo):
    id: str
    level: int = 1
    main_affix_id: Optional[str] = None
    sub_affix_info: List[SubAffixInfo] = []


class LightConeBasicInfo(BaseInfo):
    id: str
    rank: int = 1
    level: int = 1
    promotion: int = 0


class CharacterBasicInfo(BaseInfo):
    id: str
    rank: int = 0
    level: int = 1
    promotion: int = 0
    skill_tree_levels: List[LevelInfo] = []
    light_cone: Optional[LightConeBasicInfo] = None
    relics: Optional[List[RelicBasicInfo]] = None


class RelicInfo(BaseInfo):
    id: str
    name: str
    set_id: str
    set_name: str
    rarity: int
    level: int
    icon: str
    main_affix: Optional[PropertyInfo] = None
    sub_affix: List[PropertyInfo] = []


class RelicSetInfo(BaseInfo):
    id: str
    name: str
    desc: str = ""
    properties: List[PropertyInfo] = []


class LightConeInfo(BaseInfo):
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


class CharacterInfo(BaseInfo):
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
    element: Optional[ElementInfo] = None
    skills: List[SkillInfo] = []
    light_cone: Optional[LightConeInfo] = None
    relics: List[RelicInfo] = []
    relic_sets: List[RelicSetInfo] = []
    attributes: List[AttributeInfo] = []
    additions: List[AttributeInfo] = []
    properties: List[PropertyInfo] = []
