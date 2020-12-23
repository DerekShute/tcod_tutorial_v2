from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int):
        self.max_hp = hp
        self._hp = hp
        self.base_defense = base_defense
        self.base_power = base_power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def power(self) -> int:
        return self.base_power + self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    @property
    def power_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.power_bonus
        else:
            return 0

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.parent.message(death_message, death_message_color)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self,
                    amount: int,
                    msg: str,
                    source_entity: Entity=None,
                    ignore_defense: bool=False,
                    msg2: str='') -> None:
        """
        General "gets hurt" collection point
        
        'msg' is assumed to be a colorful description of the damaging action
        and possibly the instigator name.

        'msg2' is more color text going after the name of this entity.

        So the final output is: {msg} the {my name} {msg2} for {damage or no damage}

        In the future we can have different defense levels depending upon
        attack type.
        """
        if source_entity is self.engine.player:
            col = color.player_atk
        else:
            col = color.enemy_atk

        if msg2:
            desc = f'{msg} the {self.parent.name} {msg2}'
        else:
            desc = f'{msg} the {self.parent.name}'
            
        defense = 0 if ignore_defense else self.defense
        damage = max(amount - defense, 0)
        if damage > 0:
            desc = f'{desc} for {damage} hit points.'
        else:
            desc = f'{desc} but does no damage.'
        
        self.parent.message(desc, fg=col)

        self.hp -= damage  # Could call die()
        if self.hp == 0 and source_entity:
            source_entity.level.add_xp(self.parent.level.xp_given)
