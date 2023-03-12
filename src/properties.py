##########################################
# Property enumerator class for entities #
##########################################

from enum import Enum

class Context(Enum):
    DEFAULT = 0
    MESSAGES = 1
    INVENTORY = 2

class Tag(Enum):
    # used for classes of creatures to attack - Enemies vs. neutrals vs. allied
    ENEMY = 1
    NEUTRAL = 2
    ALLIED = 3

class Property(Enum):
    # ENTITIES
    NOTHING     = 0
    WALL        = 1
    WALL_PIECE  = 2
    FLOOR       = 3
    UPSTAIR     = 4
    DOWNSTAIR   = 5
    TORCH       = 6

    # FLUID
    BLOOD       = 50

    # ACTORS
    PLAYER      = 100
    WASP        = 101
    GOBLIN_SCOUT= 102

    # ITEMS
    WEAPON      = 1001
    RING        = 1002
    ARMOR       = 1003
    PROJECTILE  = 1004
    LAUNCHER    = 1005

def InfoFinder(obj_prop):
    if obj_prop == Property.NOTHING:
        return "Nothing"
    elif obj_prop == Property.WALL:
        return "Wall"
    elif obj_prop == Property.WALL_PIECE:
        return "Wall"
    elif obj_prop == Property.FLOOR:
        return "Floor"
    elif obj_prop == Property.UPSTAIR:
        return "Upstair"
    elif obj_prop == Property.DOWNSTAIR:
        return "Downstair"
    elif obj_prop == Property.TORCH:
        return "Torch"