import math
from pathlib import Path
from typing import List, Optional

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
    CharacterBasicInfo,
    CharacterInfo,
    ElementInfo,
    LevelInfo,
    LightConeBasicInfo,
    LightConeInfo,
    PathInfo,
    PropertyInfo,
    SkillInfo,
    SubAffixInfo,
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

    def __init__(self, folder: Path) -> None:
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
        self.paths = decode_json(folder / "paths.json", PathIndex)
        self.elements = decode_json(folder / "elements.json", ElementIndex)
        self.properties = decode_json(folder / "properties.json", PropertyIndex)

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
        info = CharacterInfo(basic)
        if info.id not in self.characters:
            return None
        info.name = self.characters[info.id].name
        info.rarity = self.characters[info.id].rarity
        info.path = self.get_path_info(self.characters[info.id].path)
        info.element = self.get_element_info(self.characters[info.id].element)
        skill_levels = self.merge_character_skill_upgrade(
            [
                self.get_character_skill_upgrade_from_rank(info.id, info.rank),
                self.get_character_skill_upgrade_from_skill_tree(
                    info.id, info.skill_tree_levels
                ),
            ]
        )
        info.skills = self.get_character_skill_info(info.id, skill_levels)
        info.attributes = self.get_character_attribute_from_promotion(
            info.id, info.promotion, info.level
        )
        info.properties = []

        return info

    def get_light_cone_info(self, basic: LightConeBasicInfo) -> Optional[LightConeInfo]:
        """
        Get light cone info by light cone basic info.
        """
        info = LightConeInfo(basic)
        if info.id not in self.light_cones:
            return None
        info.name = self.light_cones[info.id].name
        info.rarity = self.light_cones[info.id].rarity
        info.path = self.get_path_info(self.light_cones[info.id].path)
        info.icon = self.light_cones[info.id].icon
        info.attributes = self.get_light_cone_attribute_from_promotion(
            info.id, info.promotion, info.level
        )
        info.properties = []
        return info

    # internal methods

    def get_character_skill_info(
        self, id: str, skill_levels: List[LevelInfo]
    ) -> List[SkillInfo]:
        if id not in self.characters:
            return []
        skill_info_dict = {}
        for skill_level in skill_levels:
            if skill_level.id not in self.character_skills:
                continue
            skill = self.character_skills[skill_level.id]
            skill_info = SkillInfo()
            skill_info.id = skill_level.id
            skill_info.name = skill.name
            skill_info.level = skill_level.level
            skill_info.max_level = skill.max_level
            skill_info.element = self.get_element_info(skill.element)
            skill_info.type = skill.type
            skill_info.type_text = skill.type_text
            skill_info.effect = skill.effect
            skill_info.effect_text = skill.effect_text
            skill_info.simple_desc = skill.simple_desc
            skill_info.desc = self.format_template(
                skill.desc, skill.params[skill_level.level - 1]
            )
            skill_info.icon = skill.icon
            skill_info_dict[skill_level.id] = skill_info
        skill_info_list = []
        for skill_id in self.characters[id].skills:
            if skill_id in skill_info_dict:
                skill_info_list.append(skill_info_dict[skill_id])
            else:
                skill = self.character_skills[skill_id]
                skill_info = SkillInfo()
                skill_info.id = skill_id
                skill_info.name = skill_id
                skill_info.level = 0
                skill_info.max_level = skill.max_level
                skill_info.element = self.get_element_info(skill.element)
                skill_info.type = skill.type
                skill_info.type_text = skill.type_text
                skill_info.effect = skill.effect
                skill_info.effect_text = skill.effect_text
                skill_info.simple_desc = skill.simple_desc
                skill_info.desc = ""
                skill_info.icon = skill.icon
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
                    k,
                    property.name,
                    property.icon,
                    v.base + v.step * (level - 1),
                    self.attribute_display_format(k, v.base + v.step * (level - 1)),
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
                    k,
                    property.name,
                    property.icon,
                    v.base + v.step * (level - 1),
                    self.attribute_display_format(k, v.base + v.step * (level - 1)),
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
                    attribute_dict[attribute.field]["origin"] = attribute
                else:
                    attribute_dict[attribute.field]["value"] += attribute.value
        attribute_res = []
        for v in attribute_dict.values():
            attribute_info = v["origin"]
            attribute_info.value = v["value"]
            attribute_res.append(attribute_info)
        return attribute_res

    def merge_property(
        self, properties: List[List[PropertyInfo]]
    ) -> List[PropertyInfo]:
        """
        Merge properties.
        """
        return []

    def attribute_display_format(self, field: str, value: float) -> str:
        """
        Attribute display format.
        """
        if field in {"hp", "atk", "def", "spd"}:
            return f"{math.floor(value)}"
        else:
            return f"{math.floor(value*100)}%"

    def format_template(self, template: str, params: List[float]) -> str:
        """
        Format string template with params.
        """
        for n in range(1, 11):
            if f"#{n}[i]%" in template:
                template = template.replace(
                    f"#{n}[i]%", f"{math.floor(params[n-1]*100)}%"
                )
            if f"#{n}[i]" in template:
                template = template.replace(f"#{n}[i]", f"{math.floor(params[n-1])}")
            for f in range(1, 5):
                if f"#{n}[f{f}]%" in template:
                    template = template.replace(
                        f"#{n}[f{f}]%", f"{format(params[n-1]*100), f'.{f}f'}%"
                    )
                if f"#{n}[f{f}]" in template:
                    template = template.replace(
                        f"#{n}[f{f}]", f"{format(params[n-1]), f'.{f}f'}"
                    )
        return template
