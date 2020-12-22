from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

ARMOR_CHAR = '['
ARMOR_COLOR = (139, 69, 19)  # brown
POTION_CHAR = '!'
SCROLL_CHAR = '~'
SHIELD_CHAR = ')'
SHIELD_COLOR = (0, 191, 255)  # Light blue
WEAPON_CHAR = '/'
WEAPON_COLOR = (0, 191, 255)  # Light blue

# ===== ACTORS =====

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

def make_enemy(hp:int=1, base_defense:int=0, base_power:int=0, xp_given:int=0, **kwargs):
    return Actor(fighter=Fighter(hp=hp, base_defense=base_defense, base_power=base_power),
                 inventory=Inventory(capacity=0),
                 equipment=Equipment(),
                 ai_cls=HostileEnemy,
                 level=Level(xp_given=xp_given),
                 **kwargs
                 )

giant = make_enemy(char='G',
                   name='Giant',
                   color=(0, 127, 0),
                   hp=30,
                   base_defense=4,
                   base_power=8,
                   xp_given=200)


orc = make_enemy(char='o',
                 name='Orc',
                 color=(63, 127, 63),
                 hp=10,
                 base_power=3,
                 xp_given=35)


troll = make_enemy(char='T',
                   name='Troll',
                   color=(0, 127, 0),
                   hp=16,
                   base_defense=1,
                   base_power=4,
                   xp_given=100)


# ===== CONSUMABLES

confusion_scroll = Item(
    char=SCROLL_CHAR,
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char=SCROLL_CHAR,
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

health_potion = Item(
    char=POTION_CHAR,
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char=SCROLL_CHAR,
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)


# ===== WEAPONS

def make_weapon(name:str, **kwargs):
    return Item(char=WEAPON_CHAR, color=WEAPON_COLOR, name=name, equippable=equippable.Weapon(**kwargs))

dagger = make_weapon("Dagger", power_bonus=2)

sword = make_weapon("Sword", power_bonus=4)


# ===== ARMOR

def make_armor(name:str, **kwargs):
    return Item(char=ARMOR_CHAR, color=ARMOR_COLOR, name=name, equippable=equippable.Armor(**kwargs))

leather_armor = make_armor("Leather Armor", defense_bonus=1)

chain_mail = make_armor("Chain Mail", defense_bonus=3)

plate_mail = make_armor("Plate Mail", defense_bonus=5)


# ===== SHIELDS

def make_shield(name:str, **kwargs):
    return Item(char=SHIELD_CHAR, color=SHIELD_COLOR, name=name, equippable=equippable.Shield(**kwargs))

shield = make_shield("Shield", defense_bonus=1, power_bonus=1)

# EOF
