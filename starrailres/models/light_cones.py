from typing import Dict, List

from msgspec import Struct

from .common import Promotion, Property, Quantity


class LightConeType(Struct):
    id: str
    name: str
    rarity: int
    path: str
    icon: str
    guide_overview: List[str]


class LightConeRankType(Struct):
    id: str
    skill: str
    desc: str
    params: List[List[float]]
    properties: List[List[Property]]


class LightConePromotionType(Struct):
    id: str
    values: List[Dict[str, Promotion]]
    materials: List[List[Quantity]]


LightConeIndex = Dict[str, LightConeType]
LightConeRankIndex = Dict[str, LightConeRankType]
LightConePromotionIndex = Dict[str, LightConePromotionType]
