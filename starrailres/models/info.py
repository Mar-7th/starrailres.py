from typing import List, Optional


class LevelInfo:
    id: str
    level: int = 0

    def __init__(self, id: str, level: int = 0) -> None:
        self.id = id
        self.level = level

    def __repr__(self) -> str:
        return f"LevelInfo(id={self.id}, level={self.level})"


class PathInfo:
    id: str
    name: str
    icon: str

    def __init__(self, id: str, name: str, icon: str) -> None:
        self.id = id
        self.name = name
        self.icon = icon

    def __repr__(self) -> str:
        return f"PathInfo(id={self.id}, name={self.name}, icon={self.icon})"


class ElementInfo:
    id: str
    name: str
    color: str
    icon: str

    def __init__(self, id: str, name: str, color: str, icon: str) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.icon = icon

    def __repr__(self) -> str:
        return f"ElementInfo(id={self.id}, name={self.name}, color={self.color}, icon={self.icon})"


class SkillInfo:
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

    def __repr__(self) -> str:
        return f"SkillInfo(id={self.id}, name={self.name}, level={self.level}, max_level={self.max_level}, element={self.element}, type={self.type}, type_text={self.type_text}, effect={self.effect}, effect_text={self.effect_text}, simple_desc={self.simple_desc}, desc={self.desc}, icon={self.icon})"


class PropertyInfo:
    type: str
    name: int
    icon: str
    value: float
    display: str

    def __init__(
        self, type: str, name: int, icon: str, value: float, display: str
    ) -> None:
        self.type = type
        self.name = name
        self.icon = icon
        self.value = value
        self.display = display

    def __repr__(self) -> str:
        return f"PropertyInfo(type={self.type}, name={self.name}, icon={self.icon}, value={self.value}, display={self.display})"


class AttributeInfo:
    field: str
    name: str
    icon: str
    value: float
    display: str

    def __init__(
        self, field: str, name: str, icon: str, value: float, display: str
    ) -> None:
        self.field = field
        self.name = name
        self.icon = icon
        self.value = value
        self.display = display

    def __repr__(self) -> str:
        return f"AttributeInfo(field={self.field}, name={self.name}, icon={self.icon}, value={self.value}, display={self.display})"


class AffixInfo:
    field: str
    name: str
    value: float
    display: str
    icon: str

    def __init__(self, field: str, name: str, value: float, display: str) -> None:
        self.field = field
        self.name = name
        self.value = value
        self.display = display

    def __repr__(self) -> str:
        return f"AffixInfo(field={self.field}, name={self.name}, value={self.value}, display={self.display})"


class SubAffixInfo:
    id: str
    cnt: int
    step: int

    def __init__(self, id: str, cnt: int = 0, step: int = 0) -> None:
        self.id = id
        self.cnt = cnt
        self.step = step

    def __repr__(self) -> str:
        return f"SubAffixInfo(id={self.id}, cnt={self.cnt}, step={self.step})"


class CharacterBasicInfo:
    id: str
    rank: int
    level: int
    promotion: int
    skill_tree_levels: List[LevelInfo] = []

    def __init__(
        self,
        id: str,
        rank: int = 0,
        level: int = 1,
        promotion: int = 0,
        skill_tree_levels: List[LevelInfo] = [],
    ) -> None:
        self.id = id
        self.rank = rank
        self.level = level
        self.promotion = promotion
        self.skill_tree_levels = skill_tree_levels

    def __repr__(self) -> str:
        return f"CharacterBasicInfo(id={self.id}, rank={self.rank}, level={self.level}, promotion={self.promotion}, skill_tree_levels={self.skill_tree_levels})"


class LightConeBasicInfo:
    id: str
    rank: int
    level: int
    promotion: int

    def __init__(
        self, id: str, rank: int = 1, level: int = 1, promotion: int = 0
    ) -> None:
        self.id = id
        self.rank = rank
        self.level = level
        self.promotion = promotion

    def __repr__(self) -> str:
        return f"LightConeBasicInfo(id={self.id}, rank={self.rank}, level={self.level}, promotion={self.promotion})"


class RelicBasicInfo:
    id: str
    level: int
    main_affix_id: str
    sub_affix_info: List[SubAffixInfo]

    def __init__(
        self,
        id: str,
        level: int = 1,
        main_affix_id: str = "",
        sub_affix_info: List[SubAffixInfo] = [],
    ) -> None:
        self.id = id
        self.level = level
        self.main_affix_id = main_affix_id
        self.sub_affix_info = sub_affix_info

    def __repr__(self) -> str:
        return f"RelicBasicInfo(id={self.id}, level={self.level}, main_affix_id={self.main_affix_id}, sub_affix_info={self.sub_affix_info})"


class CharacterInfo(CharacterBasicInfo):
    name: str
    rarity: int
    path: Optional[PathInfo]
    element: Optional[ElementInfo]
    skills: List[SkillInfo]
    attributes: List[AttributeInfo]
    properties: List[PropertyInfo]

    def __init__(self, basic: CharacterBasicInfo) -> None:
        super().__init__(**basic.__dict__)

    def __repr__(self) -> str:
        return f"CharacterInfo(id={self.id}, rank={self.rank}, level={self.level}, promotion={self.promotion}, name={self.name}, rarity={self.rarity}, path={self.path}, element={self.element}, skills={self.skills}, attributes={self.attributes}, properties={self.properties})"


class LightConeInfo(LightConeBasicInfo):
    name: str
    rarity: int
    path: Optional[PathInfo]
    icon: str
    attributes: List[AttributeInfo]
    properties: List[PropertyInfo]

    def __init__(self, basic: LightConeBasicInfo) -> None:
        super().__init__(**basic.__dict__)

    def __repr__(self) -> str:
        return f"LightConeInfo(id={self.id}, rank={self.rank}, level={self.level}, promotion={self.promotion}, name={self.name}, rarity={self.rarity}, path={self.path}, icon={self.icon}, attributes={self.attributes}, properties={self.properties})"


class RelicInfo(RelicBasicInfo):
    name: str
    rarity: int
    path: PathInfo
    icon: str
    main_affix: AffixInfo
    sub_affix: List[AffixInfo]
    properties: List[PropertyInfo]

    def __init__(self, basic: RelicBasicInfo) -> None:
        super().__init__(**basic.__dict__)

    def __repr__(self) -> str:
        return f"RelicInfo(id={self.id}, level={self.level}, name={self.name}, rarity={self.rarity}, path={self.path}, icon={self.icon}, main_affix={self.main_affix}, sub_affix={self.sub_affix}, properties={self.properties})"
