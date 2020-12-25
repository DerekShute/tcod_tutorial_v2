"""
Generalized "effects" library that can be invoked as creature attacks,
consumables, traps, etc.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import color
import components.ai

if TYPE_CHECKING:
    from entity import Actor, Item, Callable


# ===== SPECIFIC EFFECTS =====

def confusion(target: Actor, duration: int) -> None:
    """
    Confusion effect to specified target entity
    
    In the future, this could be applied to the player
    """
    target.message(
        f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
        color.status_effect_applied,
    )
    target.ai = components.ai.ConfusedEnemy(
        entity=target, previous_ai=target.ai, turns_remaining=duration,
    )


def fire(target: Actor, damage: int, **kwargs) -> None:
    """
    Fire (burn) effect to specified target entity
    """
    target.fighter.take_damage(damage, "A fiery explosion engulfs", ignore_defense=True, **kwargs)


def lightning(target: Actor, damage: int, **kwargs) -> None:
    """
    Electrical (zap) effect to specified target entity
    """
    msg = "A lightning bolt strikes"
    msg2 = "with a loud thunder"
    target.fighter.take_damage(damage, msg, msg2=msg2, ignore_defense=True, **kwargs)
 
 
# ===== AREA OF EFFECT =====

def radius_aoe(engine: Engine, target_xy: Tuple[int,int], radius: int, caused_effect: Callable) -> bool:
    """
    Radius effect to target location.
    
    Returns boolean reflecting any target hit.
    """
    targets_hit = False
    for actor in engine.game_map.actors:
        if actor.distance(*target_xy) <= radius:
            caused_effect(actor)
            targets_hit = True
    return targets_hit


def nearest_aoe(engine: Engine, source_xy: Tuple[int,int], max_range: int, caused_effect: Callable, not_actor: Actor = None) -> bool:
    """
    Nearest-to-position effect.

    Returns boolean reflecting any target hit.
    """
    closest_distance = max_range + 1.0
    target = None
    for actor in engine.game_map.actors:
        if actor is not not_actor:
            distance = actor.distance(*source_xy)
            if distance < closest_distance:
                target = actor
                closest_distance = distance
    if target:
        caused_effect(target)
        return True
    return False

# EOF
