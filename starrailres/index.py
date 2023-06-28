import math
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Optional

from .models.avatars import AvatarIndex
from .models.characters import (
    CharacterIndex,
    CharacterPromotionIndex,
    CharacterRankIndex,
    CharacterSkillIndex,
    CharacterSkillTreeIndex,
)
from .models.elements import ElementIndex
from .models.info import (
    AttributeInfo,
    AvatarInfo,
    CharacterBasicInfo,
    CharacterInfo,
    ElementInfo,
    LevelInfo,
    LightConeBasicInfo,
    LightConeInfo,
    PathInfo,
    PropertyInfo,
    RelicBasicInfo,
    RelicInfo,
    RelicSetInfo,
    SkillInfo,
    SkillTreeInfo,
    SubAffixInfo,
    SubAffixBasicInfo,
)
from .models.light_cones import (
    LightConeIndex,
    LightConePromotionIndex,
    LightConeRankIndex,
)
from .models.paths import PathIndex
from .models.properties import PropertyIndex
from .models.relics import (
    RelicIndex,
    RelicMainAffixIndex,
    RelicSetIndex,
    RelicSubAffixIndex,
)
from .utils import decode_json


class Index:
    characters: CharacterIndex
    character_ranks: CharacterRankIndex
    character_skills: CharacterSkillIndex
    character_skill_trees: CharacterSkillTreeIndex
    character_promotions: CharacterPromotionIndex
    light_cones: LightConeIndex
    light_cone_ranks: LightConeRankIndex
    light_cone_promotions: LightConePromotionIndex
    relics: RelicIndex
    relic_sets: RelicSetIndex
    relic_main_affixes: RelicMainAffixIndex
    relic_sub_affixes: RelicSubAffixIndex
    paths: PathIndex
    elements: ElementIndex
    properties: PropertyIndex
    avatars: AvatarIndex

    def __init__(self, folder: Path) -> None:
        if not folder.exists():
            raise Exception("Please select an existing index folder!")
        self.characters = decode_json(folder / "characters.json", CharacterIndex)
        self.character_ranks = decode_json(
            folder / "character_ranks.json", CharacterRankIndex
        )
        self.character_skills = decode_json(
            folder / "character_skills.json", CharacterSkillIndex
        )
        self.character_skill_trees = decode_json(
            folder / "character_skill_trees.json", CharacterSkillTreeIndex
        )
        self.character_promotions = decode_json(
            folder / "character_promotions.json", CharacterPromotionIndex
        )
        self.light_cones = decode_json(folder / "light_cones.json", LightConeIndex)
        self.light_cone_ranks = decode_json(
            folder / "light_cone_ranks.json", LightConeRankIndex
        )
        self.light_cone_promotions = decode_json(
            folder / "light_cone_promotions.json", LightConePromotionIndex
        )
        self.relics = decode_json(folder / "relics.json", RelicIndex)
        self.relic_sets = decode_json(folder / "relic_sets.json", RelicSetIndex)
        self.relic_main_affixes = decode_json(
            folder / "relic_main_affixes.json", RelicMainAffixIndex
        )
        self.relic_sub_affixes = decode_json(
            folder / "relic_sub_affixes.json", RelicSubAffixIndex
        )
        self.paths = decode_json(folder / "paths.json", PathIndex)
        self.elements = decode_json(folder / "elements.json", ElementIndex)
        self.properties = decode_json(folder / "properties.json", PropertyIndex)
        self.avatars = decode_json(folder / "avatars.json", AvatarIndex)

    def get_avatar_info(self, id: str) -> Optional[AvatarInfo]:
        """
        Get avatar info by avatar id.
        """
        if id not in self.avatars:
            return None
        return AvatarInfo(
            id=id,
            name=self.avatars[id].name,
            icon=self.avatars[id].icon,
        )

    def get_path_info(self, id: str) -> Optional[PathInfo]:
        """
        Get path info by path id.
        """
        if id in self.paths:
            return PathInfo(id, self.paths[id].name, self.paths[id].icon)
        return None

    def get_element_info(self, id: str) -> Optional[ElementInfo]:
        """
        Get element info by element id.
        """
        if id not in self.elements:
            return None
        return ElementInfo(
            id, self.elements[id].name, self.elements[id].color, self.elements[id].icon
        )

    def get_character_info(self, basic: CharacterBasicInfo) -> Optional[CharacterInfo]:
        """
        Get character info by character basic info.
        """
        if basic.id not in self.characters:
            return None
        info = CharacterInfo(
            id=basic.id,
            rank=basic.rank,
            level=basic.level,
            promotion=basic.promotion,
            name=self.characters[basic.id].name,
            rarity=self.characters[basic.id].rarity,
            icon=self.characters[basic.id].icon,
            preview=self.characters[basic.id].preview,
            portrait=self.characters[basic.id].portrait,
            rank_icons=[
                self.character_ranks[i].icon for i in self.characters[basic.id].ranks
            ],
            path=self.get_path_info(self.characters[basic.id].path),
            element=self.get_element_info(self.characters[basic.id].element),
            skills=self.get_character_skill_info(
                basic.id,
                self.merge_character_skill_upgrade(
                    [
                        self.get_character_skill_upgrade_from_rank(
                            basic.id, basic.rank
                        ),
                        self.get_character_skill_upgrade_from_skill_tree(
                            basic.id, basic.skill_tree_levels
                        ),
                    ]
                ),
            ),
            skill_trees=[
                SkillTreeInfo(
                    id=i.id,
                    level=i.level,
                    icon=self.character_skill_trees[i.id].icon,
                )
                for i in basic.skill_tree_levels
            ],
            light_cone=None,
            relics=[],
            relic_sets=[],
            attributes=self.get_character_attribute_from_promotion(
                basic.id, basic.promotion, basic.level
            ),
            additions=[],
            properties=self.merge_property(
                [
                    self.get_character_property_from_skill_tree(
                        basic.id, basic.skill_tree_levels
                    )
                ]
            ),
        )
        # light cone
        info.light_cone = (
            self.get_light_cone_info(basic.light_cone) if basic.light_cone else None
        )
        # relics
        relic_infos = (
            (self.get_relic_info(relic) for relic in basic.relics)
            if basic.relics
            else []
        )
        info.relics = [
            relic_info for relic_info in relic_infos if relic_info is not None
        ]
        # relic sets
        info.relic_sets = self.get_relic_sets_info(info.relics) if info.relics else []
        # attributes
        info.attributes = self.merge_attribute(
            [
                info.attributes,
                info.light_cone.attributes if info.light_cone else [],
            ]
        )
        # properties
        relic_properties = []
        for relic in info.relics:
            if relic.main_affix:
                relic_properties.append(relic.main_affix)
            relic_properties += relic.sub_affix
        for relic_set in info.relic_sets:
            relic_properties += relic_set.properties
        info.properties = self.merge_property(
            [
                info.properties,
                info.light_cone.properties if info.light_cone else [],
                relic_properties,
            ]
        )
        # additions
        info.additions = self.calculate_additions(info.attributes, info.properties)
        return info

    def get_light_cone_info(self, basic: LightConeBasicInfo) -> Optional[LightConeInfo]:
        """
        Get light cone info by light cone basic info.
        """
        if basic.id not in self.light_cones:
            return None
        info = LightConeInfo(
            id=basic.id,
            rank=basic.rank,
            level=basic.level,
            promotion=basic.promotion,
            name=self.light_cones[basic.id].name,
            rarity=self.light_cones[basic.id].rarity,
            path=self.get_path_info(self.light_cones[basic.id].path),
            icon=self.light_cones[basic.id].icon,
            preview=self.light_cones[basic.id].preview,
            portrait=self.light_cones[basic.id].portrait,
            attributes=self.get_light_cone_attribute_from_promotion(
                basic.id, basic.promotion, basic.level
            ),
            properties=self.merge_property(
                [self.get_light_cone_property_from_rank(basic.id, basic.rank)]
            ),
        )
        return info

    def get_relic_info(self, basic: RelicBasicInfo) -> Optional[RelicInfo]:
        if basic.id not in self.relics:
            return None
        info = RelicInfo(
            id=basic.id,
            name=self.relics[basic.id].name,
            set_id=self.relics[basic.id].set_id,
            set_name=self.relic_sets[self.relics[basic.id].set_id].name,
            rarity=self.relics[basic.id].rarity,
            level=basic.level,
            icon=self.relics[basic.id].icon,
            main_affix=self.get_relic_main_affix(
                basic.id, basic.level, basic.main_affix_id
            ),
            sub_affix=self.get_relic_sub_affix(basic.id, basic.sub_affix_info),
        )
        return info

    def get_relic_sets_info(self, relics: List[RelicInfo]) -> List[RelicSetInfo]:
        set_num: Dict[str, int] = {}
        for relic in relics:
            if relic.set_id not in set_num:
                set_num[relic.set_id] = 1
            else:
                set_num[relic.set_id] += 1
        relic_sets = []
        for k, v in set_num.items():
            if v >= 2:
                relic_sets.append(
                    RelicSetInfo(
                        id=k,
                        name=self.relic_sets[k].name,
                        icon=self.relic_sets[k].icon,
                        num=2,
                        desc=self.relic_sets[k].desc[0],
                        properties=[
                            PropertyInfo(
                                type=i.type,
                                field=self.properties[i.type].field,
                                name=self.properties[i.type].name,
                                icon=self.properties[i.type].icon,
                                value=i.value,
                                display=self.value_display_format(
                                    i.value,
                                    self.properties[i.type].percent,
                                ),
                                percent=self.properties[i.type].percent,
                            )
                            for i in self.relic_sets[k].properties[0]
                        ],
                    )
                )
            if v >= 4:
                relic_sets.append(
                    RelicSetInfo(
                        id=k,
                        name=self.relic_sets[k].name,
                        icon=self.relic_sets[k].icon,
                        num=4,
                        desc=self.relic_sets[k].desc[1]
                        if len(self.relic_sets[k].desc) > 1
                        else "",
                        properties=[
                            PropertyInfo(
                                type=i.type,
                                field=self.properties[i.type].field,
                                name=self.properties[i.type].name,
                                icon=self.properties[i.type].icon,
                                value=i.value,
                                display=self.value_display_format(
                                    i.value,
                                    self.properties[i.type].percent,
                                ),
                                percent=self.properties[i.type].percent,
                            )
                            for i in (
                                self.relic_sets[k].properties[1]
                                if len(self.relic_sets[k].properties) > 1
                                else []
                            )
                        ],
                    )
                )
        return relic_sets

    # internal methods

    def get_character_skill_info(
        self, id: str, skill_levels: List[LevelInfo]
    ) -> List[SkillInfo]:
        """
        Get character skill info by character id and skill levels.
        """
        if id not in self.characters:
            return []
        skill_info_dict = {}
        for skill_level in skill_levels:
            if skill_level.id not in self.character_skills:
                continue
            skill = self.character_skills[skill_level.id]
            params = skill.params[skill_level.level - 1] if skill.params else []
            skill_info = SkillInfo(
                id=skill_level.id,
                name=skill.name,
                level=skill_level.level,
                max_level=skill.max_level,
                element=self.get_element_info(skill.element),
                type=skill.type,
                type_text=skill.type_text,
                effect=skill.effect,
                effect_text=skill.effect_text,
                simple_desc=skill.simple_desc,
                desc=self.format_template(skill.desc, params),
                icon=skill.icon,
            )
            skill_info_dict[skill_level.id] = skill_info
        skill_info_list = []
        for skill_id in self.characters[id].skills:
            if skill_id in skill_info_dict:
                skill_info_list.append(skill_info_dict[skill_id])
            else:
                skill = self.character_skills[skill_id]
                skill_info = SkillInfo(
                    id=skill_id,
                    name=skill_id,
                    level=0,
                    max_level=skill.max_level,
                    element=self.get_element_info(skill.element),
                    type=skill.type,
                    type_text=skill.type_text,
                    effect=skill.effect,
                    effect_text=skill.effect_text,
                    simple_desc=skill.simple_desc,
                    desc="",
                    icon=skill.icon,
                )
                skill_info_list.append(skill_info)
        return skill_info_list

    def get_character_attribute_from_promotion(
        self, id: str, promotion: int, level: int
    ) -> List[AttributeInfo]:
        """
        Get character attribute from promotion.
        """
        if id not in self.character_promotions:
            return []
        if promotion not in range(0, 6 + 1):  # 0-6
            return []
        if level not in range(1, 80 + 1):  # 1-80
            return []
        attributes = []
        for k, v in self.character_promotions[id].values[promotion].items():
            property = None
            for i in self.properties.values():
                if i.field == k:
                    property = i
                    break
            if property is None:
                continue
            attributes.append(
                AttributeInfo(
                    field=k,
                    name=property.name,
                    icon=property.icon,
                    value=v.base + v.step * (level - 1),
                    display=self.value_display_format(
                        v.base + v.step * (level - 1), property.percent
                    ),
                    percent=property.percent,
                )
            )
        return attributes

    def get_light_cone_attribute_from_promotion(
        self, id: str, promotion: int, level: int
    ) -> List[AttributeInfo]:
        """
        Get light cone attribute from promotion.
        """
        if id not in self.light_cone_promotions:
            return []
        if promotion not in range(0, 6 + 1):  # 0-6
            return []
        if level not in range(1, 80 + 1):  # 1-80
            return []
        attributes = []
        for k, v in self.light_cone_promotions[id].values[promotion].items():
            property = None
            for i in self.properties.values():
                if i.field == k:
                    property = i
                    break
            if property is None:
                continue
            attributes.append(
                AttributeInfo(
                    field=k,
                    name=property.name,
                    icon=property.icon,
                    value=v.base + v.step * (level - 1),
                    display=self.value_display_format(
                        v.base + v.step * (level - 1), property.percent
                    ),
                    percent=property.percent,
                )
            )
        return attributes

    def get_character_skill_upgrade_from_rank(
        self, id: str, rank: int
    ) -> List[LevelInfo]:
        """
        Get character skill upgrade from rank.
        """
        if id not in self.characters:
            return []
        if rank not in range(0, 6 + 1):  # 0-6
            return []
        unlock_ranks = self.characters[id].ranks[:rank]
        skill_upgrades = []
        for unlock_rank in unlock_ranks:
            if unlock_rank in self.character_ranks:
                skill_up_list = self.character_ranks[unlock_rank].level_up_skills
                for skill_up in skill_up_list:
                    skill_upgrades.append(LevelInfo(skill_up.id, skill_up.num))
        return skill_upgrades

    def get_character_skill_upgrade_from_skill_tree(
        self, id: str, skill_tree_levels: List[LevelInfo]
    ) -> List[LevelInfo]:
        """
        Get character skill upgrade from skill tree.
        """
        if id not in self.characters:
            return []
        skill_trees = self.characters[id].skill_trees
        skill_upgrades = []
        for skill_tree in skill_tree_levels:
            if (
                skill_tree.id in skill_trees
                and skill_tree.id in self.character_skill_trees
            ):
                skill_up_list = self.character_skill_trees[
                    skill_tree.id
                ].level_up_skills
                for skill_up in skill_up_list:
                    skill_upgrades.append(
                        LevelInfo(skill_up.id, skill_up.num * skill_tree.level)
                    )
        return skill_upgrades

    def get_character_property_from_skill_tree(
        self, id: str, skill_tree_levels: List[LevelInfo]
    ) -> List[PropertyInfo]:
        """
        Get character property from skill tree.
        """
        if id not in self.characters:
            return []
        skill_trees = self.characters[id].skill_trees
        properties = []
        for skill_tree in skill_tree_levels:
            if (
                skill_tree.id in skill_trees
                and skill_tree.id in self.character_skill_trees
            ):
                property_list = (
                    self.character_skill_trees[skill_tree.id]
                    .levels[skill_tree.level - 1]
                    .properties
                )
                for i in property_list:
                    if i.type not in self.properties:
                        continue
                    property = self.properties[i.type]
                    properties.append(
                        PropertyInfo(
                            type=i.type,
                            field=property.field,
                            name=property.name,
                            icon=property.icon,
                            value=i.value,
                            display=self.value_display_format(
                                i.value, property.percent
                            ),
                            percent=property.percent,
                        )
                    )
        return properties

    def get_light_cone_property_from_rank(
        self, id: str, rank: int
    ) -> List[PropertyInfo]:
        """
        Get light cone property from rank.
        """
        if id not in self.light_cone_ranks:
            return []
        if rank not in range(1, 5 + 1):  # 1-5
            return []
        properties = []
        for i in self.light_cone_ranks[id].properties[rank - 1]:
            if i.type not in self.properties:
                continue
            property = self.properties[i.type]
            properties.append(
                PropertyInfo(
                    type=i.type,
                    field=property.field,
                    name=property.name,
                    icon=property.icon,
                    value=i.value,
                    display=self.value_display_format(i.value, property.percent),
                    percent=property.percent,
                )
            )
        return properties

    def get_relic_main_affix(
        self, id: str, level: int, main_affix_id: Optional[str]
    ) -> Optional[PropertyInfo]:
        """
        Get relic property from affix.
        """
        if id not in self.relics:
            return None
        if not main_affix_id:
            return None
        main_affix_group = self.relics[id].main_affix_id
        if (
            main_affix_group not in self.relic_main_affixes
            or main_affix_id not in self.relic_main_affixes[main_affix_group].affixes
        ):
            return None
        affix = self.relic_main_affixes[main_affix_group].affixes[main_affix_id]
        main_affix_info = PropertyInfo(
            type=affix.property,
            field=self.properties[affix.property].field,
            name=self.properties[affix.property].name,
            icon=self.properties[affix.property].icon,
            value=affix.base + affix.step * level,
            display=self.value_display_format(
                affix.base + affix.step * level,
                self.properties[affix.property].percent,
            ),
            percent=self.properties[affix.property].percent,
        )
        return main_affix_info

    def get_relic_sub_affix(
        self, id: str, sub_affix_info: List[SubAffixBasicInfo]
    ) -> List[SubAffixInfo]:
        """
        Get relic property from affix.
        """
        if id not in self.relics:
            return []
        sub_affix_group = self.relics[id].sub_affix_id
        if sub_affix_group not in self.relic_sub_affixes:
            return []
        properties = []
        for sub_affix in sub_affix_info:
            if sub_affix.id not in self.relic_sub_affixes[sub_affix_group].affixes:
                continue
            affix = self.relic_sub_affixes[sub_affix_group].affixes[sub_affix.id]
            properties.append(
                SubAffixInfo(
                    type=affix.property,
                    field=self.properties[affix.property].field,
                    name=self.properties[affix.property].name,
                    icon=self.properties[affix.property].icon,
                    value=affix.base * sub_affix.cnt + affix.step * sub_affix.step,
                    display=self.value_display_format(
                        affix.base * sub_affix.cnt + affix.step * sub_affix.step,
                        self.properties[affix.property].percent,
                    ),
                    percent=self.properties[affix.property].percent,
                    count=sub_affix.cnt,
                    step=sub_affix.step,
                )
            )
        return properties

    def calculate_additions(
        self, attributes: List[AttributeInfo], properties: List[PropertyInfo]
    ) -> List[AttributeInfo]:
        """
        Calculate additions from attributes and properties.
        """
        attribute_dict = {}
        addition_dict = {}
        for attribute in attributes:
            if attribute.field not in addition_dict:
                attribute_dict[attribute.field] = attribute.value
        for property in properties:
            if (
                self.properties[property.type].ratio
                and property.field in attribute_dict
            ):
                value = property.value * attribute_dict[property.field]
            else:
                value = property.value
            if property.field not in addition_dict:
                addition_dict[property.field] = value
            else:
                addition_dict[property.field] += value
        additions = []
        for k, v in addition_dict.items():
            property = None
            for i in self.properties.values():
                if i.field == k:
                    property = i
                    break
            if property is None:
                continue
            additions.append(
                AttributeInfo(
                    field=k,
                    name=property.name,
                    icon=property.icon,
                    value=v,
                    display=self.value_display_format(v, property.percent),
                    percent=property.percent,
                )
            )
        return additions

    def merge_character_skill_upgrade(
        self, skill_upgrades: List[List[LevelInfo]]
    ) -> List[LevelInfo]:
        """
        Merge skill upgrades of character.
        """
        skill_upgrade_dict = {}
        for skill_list in skill_upgrades:
            for skill in skill_list:
                if skill.id not in skill_upgrade_dict:
                    skill_upgrade_dict[skill.id] = skill.level
                else:
                    skill_upgrade_dict[skill.id] += skill.level
        return [LevelInfo(id, level) for id, level in skill_upgrade_dict.items()]

    def merge_attribute(
        self, attributes: List[List[AttributeInfo]]
    ) -> List[AttributeInfo]:
        """
        Merge attributes.
        """
        attribute_dict = {}
        for attribute_list in attributes:
            for attribute in attribute_list:
                if attribute.field not in attribute_dict:
                    attribute_dict[attribute.field] = {}
                    attribute_dict[attribute.field]["value"] = attribute.value
                    attribute_dict[attribute.field]["origin"] = deepcopy(attribute)
                else:
                    attribute_dict[attribute.field]["value"] += attribute.value
        attribute_res = []
        for v in attribute_dict.values():
            attribute_info: AttributeInfo = v["origin"]
            attribute_info.value = v["value"]
            attribute_info.display = self.value_display_format(
                v["value"], attribute_info.percent
            )
            attribute_res.append(attribute_info)
        return attribute_res

    def merge_property(
        self, properties: List[List[PropertyInfo]]
    ) -> List[PropertyInfo]:
        """
        Merge properties.
        """
        property_dict = {}
        for property_list in properties:
            for property in property_list:
                if property.type not in property_dict:
                    property_dict[property.type] = {}
                    property_dict[property.type]["value"] = property.value
                    property_dict[property.type]["origin"] = deepcopy(property)
                else:
                    property_dict[property.type]["value"] += property.value
        property_res = []
        for v in property_dict.values():
            property_info: PropertyInfo = v["origin"]
            property_info.value = v["value"]
            property_info.display = self.value_display_format(
                v["value"], property_info.percent
            )
            property_res.append(property_info)
        return property_res

    def value_display_format(self, value: float, percent: bool) -> str:
        """
        Value display format.
        """
        if percent:
            return format(math.floor(value * 1000) / 10.0, ".1f") + "%"
        else:
            return f"{math.floor(value)}"

    def format_template(self, template: str, params: List[float]) -> str:
        """
        Format string template with params.
        """
        for n in range(1, 11):
            if len(params) < n:
                break
            if f"#{n}[i]%" in template:
                template = template.replace(
                    f"#{n}[i]%", f"{math.floor(params[n-1]*100)}%"
                )
            if f"#{n}[i]" in template:
                template = template.replace(f"#{n}[i]", f"{math.floor(params[n-1])}")
            for f in range(1, 5):
                if f"#{n}[f{f}]%" in template:
                    value = format(params[n - 1] * 100, f".{f}f")
                    template = template.replace(f"#{n}[f{f}]%", f"{value}%")
                if f"#{n}[f{f}]" in template:
                    value = format(params[n - 1], f".{f}f")
                    template = template.replace(f"#{n}[f{f}]", f"{value}")
        return template
