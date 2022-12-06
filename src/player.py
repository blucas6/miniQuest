from copy import deepcopy

from config import *
from colors import *
from algos import *
from icon_config import PLAYER_ICON
from properties import Property
from entity import LighMode

class Player:
    def __init__(self, game):
        self.game = game
        self.name = "Calvin"
        self.ICON = PLAYER_ICON
        self.BG = VOID
        self.FG = WHITE
        self.POS = PLAYER_ST
        self.INFO = Property.PLAYER

        # STATS
        self.str = PLAYER_ST_STRENGTH
        self.dex = PLAYER_ST_DEX
        self.luck = PLAYER_ST_LUCK

    def move(self, dir):
        if self.canMove(dir):
            self.POS[0] += dir[0]
            self.POS[1] += dir[1]
            return True
        return False

    def stairs(self, dir):
        item_list = self.game.CURRENT_LV_O.Level_Map[self.POS[1]][self.POS[0]]
        if item_list:
            for i in item_list:
                if (i.PROP == Property.UPSTAIR or i.PROP == Property.DOWNSTAIR):
                    print("compare:", i.POS, i.PROP, self.POS)
                    # Check for success
                    if i.ACTION(dir):
                        return True
        return False

    def canMove(self, d):
        lvl_o = self.game.LEVELS[self.game.CURR_LEVEL]
        if lvl_o.Tower_Map[self.POS[1] + d[1]][self.POS[0] + d[0]].isCOLL:
            return False
        tile_list = lvl_o.Level_Map[self.POS[1] + d[1]][self.POS[0] + d[0]]
        if tile_list:
            for i in tile_list:
                if i.isCOLL:
                    return False
        return True

    def FOVsight(self, level_obj):
        # access astar grid from level
        grid = deepcopy(self.game.LEVELS[self.game.CURR_LEVEL].astarGrid)
        FOV(grid, self.POS)
        # print("-----------FOV-------------")
        # for r in grid:
        #     print(r)
        for r in range(len(level_obj.Light_Map)):
            for c in range(len(level_obj.Light_Map[0])):
                if grid[r][c] == 2 or grid[r][c] == 1:
                    level_obj.Light_Map[r][c] = LighMode.SEEN
                else:
                    level_obj.Light_Map[r][c] = LighMode.UNSEEN

        
        