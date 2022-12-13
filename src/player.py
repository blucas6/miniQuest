from copy import deepcopy

from config import *
from colors import *
from algos import *
from icon_config import PLAYER_ICON
from properties import Property, Tag
from entity import LightMode

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
        self.HEALTH = PLAYER_ST_HEALTH
        self.STR = PLAYER_ST_STRENGTH
        self.DEX = PLAYER_ST_DEX
        self.LUCK = PLAYER_ST_LUCK
        self.SPEED = PLAYER_ST_SPEED

        self.next_move = [0,0]

    def update(self):
        self.POS[0] += self.next_move[0]
        self.POS[1] += self.next_move[1]
        self.next_move = [0,0]
        self.FOVsight(self.game.CURRENT_LV_O)

    def move(self, dir):
        if self.canMove(dir):
            self.next_move = dir
        else:
            self.next_move = [0,0]
        return self.SPEED       # return amount of turns taken to move

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
        for c in lvl_o.creatures:
            if c.POS[1] == self.POS[1] + d[1] and c.POS[0] == self.POS[0] + d[0]:
                self.Attack(c)
                return False
        return True

    def Attack(self, c_obj):
        c_obj.takeDmg(self.STR)

    def FOVsight(self, level_obj):
        # access astar grid from level
        grid = deepcopy(self.game.LEVELS[self.game.CURR_LEVEL].lightmode_astar)
        FOV(grid, self.POS)
        # print("-----------FOV-------------")
        # for r in grid:
        #     print(r)
        for r in range(len(level_obj.Light_Map)):
            for c in range(len(level_obj.Light_Map[0])):
                if not level_obj.Light_Map[r][c] == LightMode.LIT:
                    if grid[r][c] == 2:
                        level_obj.Light_Map[r][c] = LightMode.SEEN
                    else:
                        level_obj.Light_Map[r][c] = LightMode.UNSEEN

    def takeDmg(self, dmg):
        self.HEALTH -= dmg

        
        