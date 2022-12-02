from enum import Enum

from colors import *
from config import *
from properties import Property
from icon_config import *

class LighMode(Enum):
    UNSEEN = 1          # Icon will be turned to a unseen floor piece
    SEEN = 2            # Icon will be turned to ICON
    LIT = 3             # Icon will be turned to ICON but lightened up

class Entity:
    def __init__(self, game, prop, icon, bg, fg, col, pos):
        self.game = game
        self.ICON = icon            # coords to tileset
        self.BG = bg                # background color
        self.FG = fg                # sprite color
        self.PROP = prop            # entity enum to distinguish between different entities
        self.isCOLL = col           # is the object able to be collided with?
        self.POS = pos
        self.MODE = LighMode.UNSEEN

        self.activated = False

    def update(self):
        pass

    def ACTIVATE(self):
        # ACTIVATE functions used only once
        pass

    def ACTION(self):
        # ACTION functions can be accessed by the player
        pass

# *** TOWER *** #
class WallPiece(Entity):
    def __init__(self, game, pos):
        Entity.__init__(self, game, Property.WALL_PIECE, T_INS_WALL, VOID, WHITE, True, pos)

class Floor(Entity):
    def __init__(self, game, pos):
        Entity.__init__(self, game, Property.FLOOR, T_FLOOR_LIGHT, VOID, WHITE, False, pos)

class Wall(Entity):
    # walls cannot be destroyed otherwise FOV algo will fail
    def __init__(self, game, type, pos):
        if type == "h":
            piece = T_HWALL
        elif type == "v":
            piece = T_VWALL
        elif type == "c":
            piece = T_CURVE
        else:
            piece = PLAYER_ICON
            print("ERROR: Invalid piece given")
        Entity.__init__(self, game, Property.WALL, piece, VOID, WHITE, True, pos)

class Stair(Entity):
    def __init__(self, game, dir, pos):
        if dir == "up":
            prop = Property.UPSTAIR
            icon = UPSTAIR
        else:
            prop = Property.DOWNSTAIR
            icon = DOWNSTAIR

        Entity.__init__(self, game, prop, icon, SEABLUE, WHITE, False, pos)
    def ACTION(self, dir):
        if dir == "up" and self.INFO == Property.UPSTAIR:
            # GO UP - check if there is an above level first
            # or create new level and append to level list
            if len(self.game.LEVELS)-1 == self.game.CURR_LEVEL:
                self.game.newLevel()
            else:
                self.game.CURR_LEVEL += 1
            print("go up")
            self.game.MENUS[0].MSG_STR = "You walk up the stairs"
            return True
        elif dir == "down" and self.INFO == Property.DOWNSTAIR:
            # GO DOWN - level pointer back one
            self.game.CURR_LEVEL -= 1
            print("go down")
            self.game.MENUS[0].MSG_STR = "You descend down"
            return True
        return False

class Torch(Entity):
    def __init__(self, game, pos):
        Entity.__init__(self, game, Property.TORCH, TORCH, VOID, BROWN, False, pos)
    def ACTIVATE(self):
        if not self.activated:
            self.activated = True
    def update(self):
        if self.activated:
            self.MODE = LighMode.LIT
            # for coord in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,0], [0,1], [1,-1], [1,0], [1,1], [0,-2], [2,0], [0,2], [2,0]]:
            #     if self.POS[0] + coord[0] >= 0 and self.POS[0] + coord[0] < MAP_W-2 and self.POS[1] + coord[1] >= 0 and self.POS[1] < MAP_H-2:
            #         self.game.LEVELS[self.game.CURR_LEVEL].map[self.POS[0] + coord[0]][self.POS[1] + coord[1]].MODE    

class Void(Entity):
    def __init__(self, game, pos):
        Entity.__init__(self, game, Property.NOTHING, [0,0], VOID, WHITE, False, pos)


# *** UI ENTITIES *** #
class UI:
    def __init__(self, type):
        if type == "h":
            piece = B_HOR
        elif type == "v":
            piece = B_VERT
        elif type == "tl":
            piece = B_C_TL
        elif type == "tr":
            piece = B_C_TR
        elif type == "bl":
            piece = B_C_BL
        elif type == "br":
            piece = B_C_BR
        else:
            piece = [0,0]

        self.ICON = piece
