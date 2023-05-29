from typing import Dict, List

from msgspec import Struct

from .common import Promotion, Property, Quantity


class CharacterEvaluationType(Struct):
    image: str
    link: str


class CharacterType(Struct):
    id: str
    name: str
    tag: str
    rarity: int
    path: str
    element: str
    max_sp: float
    ranks: List[str]
    skills: List[str]
    skill_trees: List[str]
    icon: str
    preview: str
    portrait: str
    guide_overview: List[str]
    guide_material: List[str]
    guide_evaluation: List[CharacterEvaluationType]


class CharacterRankType(Struct):
    id: str
    rank: int
    desc: str
    materials: List[Quantity]
    level_up_skills: List[Quantity]
    icon: str


class CharacterSkillType(Struct):
    id: str
    name: str
    max_level: int
    element: str
    type: str
    type_text: str
    effect: str
    effect_text: str
    simple_desc: str
    desc: str
    params: List[List[float]]
    icon: str


class SkillTreeLevelType(Struct):
    promotion: int
    properties: List[Property]
    materials: List[Quantity]


class CharacterSkillTreeType(Struct):
    id: str
    max_level: int
    anchor: str
    pre_points: List[str]
    level_up_skills: List[Quantity]
    levels: List[SkillTreeLevelType]


class CharacterPromotionType(Struct):
    id: str
    values: List[Dict[str, Promotion]]
    materials: List[List[Quantity]]


CharacterIndex = Dict[str, CharacterType]
CharacterRankIndex = Dict[str, CharacterRankType]
CharacterSkillIndex = Dict[str, CharacterSkillType]
CharacterSkillTreeIndex = Dict[str, CharacterSkillTreeType]
CharacterPromotionIndex = Dict[str, CharacterPromotionType]
