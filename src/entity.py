from enum import Enum

from colors import *
from configs.config import *
from properties import Property
from configs.icon_config import *

class LightMode(Enum):
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
        self.MODE = LightMode.UNSEEN
        
        self.already_seen = False   # entities stay in sight if already seen once
        self.activated = False      # track activation of entities, only ONCE

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
        if dir == "up" and self.PROP == Property.UPSTAIR:
            self.game.changeLevel("up")
            return True
        elif dir == "down" and self.PROP == Property.DOWNSTAIR:
            self.game.changeLevel("down")
            return True
        return False

class Torch(Entity):
    def __init__(self, game, pos):
        Entity.__init__(self, game, Property.TORCH, TORCH, VOID, BROWN, False, pos)
    def ACTIVATE(self):
        if not self.activated:
            self.activated = True
            self.BG = ORANGE
    def update(self):
        if self.activated:
            self.MODE = LightMode.LIT
            for coord in [[-1,-1], [-1,0], [-1,1], [0,-1], [0,0], [0,1], [1,-1], [1,0], [1,1]]:
                row = self.POS[1] + coord[1]
                col = self.POS[0] + coord[0]
                if col >= 0 and col < MAP_W and row >= 0 and row < MAP_H and self.game.CURRENT_LV_O.Tower_Map[row][col].PROP != Property.WALL:
                    self.game.CURRENT_LV_O.Light_Map[row][col] = LightMode.LIT 
            for o_coord in [[-1,0], [1,0], [0,-1], [0,1]]:
                row = self.POS[1] + o_coord[1]
                col = self.POS[0] + o_coord[0]
                row2 = self.POS[1] + o_coord[1]*2
                col2 = self.POS[0] +o_coord[0]*2
                if col >= 0 and col < MAP_W and row >= 0 and row < MAP_H and col2 >= 0 and col2 < MAP_W and row2 >= 0 and row2 < MAP_H:
                    if self.game.CURRENT_LV_O.Light_Map[row][col] == LightMode.LIT:
                        self.game.CURRENT_LV_O.Light_Map[row2][col2] = LightMode.LIT

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
