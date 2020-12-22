from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


# ===== SUBCLASSES

class Weapon(Equippable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, *args, **kwargs)


class Armor(Equippable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, *args, **kwargs)
