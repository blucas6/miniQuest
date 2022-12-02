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
        self.str = P_ST_STRENGTH
        self.dex = P_ST_DEX
        self.luck = P_ST_LUCK


    def move(self, dir):
        if self.canMove(dir):
            self.POS[0] += dir[0]
            self.POS[1] += dir[1]
            return True
        return False
            # print(self.game.LEVELS[self.game.CURR_LEVEL].map[self.POS[1]][self.POS[0]].INFO)
            # print(self.POS)
            # for r in range(self.game.LEVELS[self.game.CURR_LEVEL].levelh+1):
            #     for c in range(self.game.LEVELS[self.game.CURR_LEVEL].levelw+1):
            #         print(self.game.LEVELS[self.game.CURR_LEVEL].map[r][c].curricon, end=" ")
            #     print("")
            # for e in self.game.LEVELS[self.game.CURR_LEVEL].entities:
            #     print(e.INFO, e.POS)

    def stairs(self, dir):
        for e in self.game.LEVELS[self.game.CURR_LEVEL].entities:
            if (e.PROP == Property.UPSTAIR or e.PROP == Property.DOWNSTAIR) and e.POS == self.POS:
                print("compare:", e.POS, e.PROP, self.POS)
                # Check for success
                if e.ACTION(dir):
                    return True
        return False

    def canMove(self, d):
        lvl_o = self.game.LEVELS[self.game.CURR_LEVEL]
        if lvl_o.Tower_Map[self.POS[1] + d[1]][self.POS[0] + d[0]].isCOLL:
            return False
        tile_list = lvl_o.Level_Map[self.POS[1] + d[1]][self.POS[0] + d[0]]
        if not tile_list:
            for i in tile_list:
                if i.isCOLL:
                    return False
        return True

    def FOVsight(self, level_obj):
        # access astar grid from level
        grid = deepcopy(self.game.LEVELS[self.game.CURR_LEVEL].astarGrid)
        FOV(grid, self.POS)
        print("------------------------")
        for r in grid:
            print(r)
        for r in range(len(level_obj.Light_Map)):
            for c in range(len(level_obj.Light_Map)):
                if grid[r][c] == 2 or grid[r][c] == 1:
                    level_obj.Light_Map[r][c] = LighMode.SEEN
                else:
                    level_obj.Light_Map[r][c] = LighMode.UNSEEN

        
        