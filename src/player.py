from copy import deepcopy
import random as rand

from configs.config import *
from colors import *
from algos import *
from configs.icon_config import PLAYER_ICON
from properties import Property, Tag
from entity import LightMode
from items import *

class Player:
    def __init__(self, game):
        self.game = game
        self.name = "Calvin"
        self.ICON = PLAYER_ICON
        self.BG = VOID
        self.FG = WHITE
        self.POS = PLAYER_ST
        self.INFO = Property.PLAYER

        # INVENTORY
        self.INVENTORY = []

        self.ARMOR = Leather_Armor()
        self.MAIN_HAND = Wooden_Sword()
        self.ALT_HAND = ""

        # STATS
        self.HEALTH = PLAYER_ST_HEALTH          # Max health
        self.CURR_HEALTH = PLAYER_ST_HEALTH     # Current health
        self.STR = PLAYER_ST_STRENGTH           # Melee weapon hit bonus, melee weapon damage bonus
        self.DEX = PLAYER_ST_DEX                # Ranged weapon hit bonus, dodgeability
        self.LUCK = PLAYER_ST_LUCK              # How lucky - enemy drops, treasure chests
        self.SPEED = PLAYER_ST_SPEED            # How fast a player moves - how much energy is given to others
        self.AC = 10                            # Natural armor class, without armor equipped

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
                self.Attack_Melee(c)
                return False
        return True

    def Attack_Melee(self, c_obj):
        damage = self.StatMod(self.STR)
        roll = rand.randint(0, 20)
        if roll == 20:
            if self.MAIN_HAND != "":
                damage += self.MAIN_HAND.MeleeDmg() + self.MAIN_HAND.MeleeDmg()
            if self.ALT_HAND != "":
                damage += self.ALT_HAND.MeleeDmg() + self.ALT_HAND.MeleeDmg()
            self.game.NewMessage("Crit! %s damage" % (damage))
            c_obj.takeDmg(damage)
        else:
            roll += self.StatMod(self.STR)
            if self.MAIN_HAND != "":
                damage += self.MAIN_HAND.MeleeDmg()
                roll += self.MAIN_HAND.MainToHit_Bonus
            if self.ALT_HAND != "":
                damage += self.ALT_HAND.MeleeDmg()
                roll += self.ALT_HAND.AltToHit_Bonus
            if roll >= c_obj.AC:
                print("Dealt", damage, "damage | roll:", roll, "| enemy ac:", c_obj.AC)
                self.game.NewMessage("Dealt %s damage" % (damage))
                c_obj.takeDmg(damage)
            else:
                self.game.NewMessage("Missed!")
                print("Missed! | roll:", roll, "| enemy ac:", c_obj.AC)
        

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

    def takeDmg(self, roll, dmg):
        current_ac = self.AC
        weight = self.InventoryWeight()
        if self.ARMOR != "":
            current_ac += self.ARMOR.ArmorClass
            weight += self.ARMOR.WEIGHT
        if self.MAIN_HAND != "":
            current_ac += self.MAIN_HAND.ArmorClass
            weight += self.MAIN_HAND.WEIGHT
        if self.ALT_HAND != "":
            current_ac += self.ALT_HAND.ArmorClass
            weight += self.ALT_HAND.WEIGHT
        
        dodge = self.StatMod(self.DEX)
        if weight >= 100 and weight < 200:
            dodge -= 1
        elif weight >= 200 and weight < 250:
            dodge -= 2
        elif weight >= 250 and weight < 300:
            dodge -= 3
        elif weight >= 300:
            dodge -= 5

        # Check if attack hits
        if roll >= current_ac + dodge:
            print("Player took:", dmg, "damage | roll:", roll, "| AC:", current_ac, " | dodge:", dodge)
            self.CURR_HEALTH -= dmg

    def takeRawDmg(self, dmg):
        self.CURR_HEALTH -= dmg

    def StatMod(self, stat):
        if stat < 3:
            return 1
        elif stat < 7:
            return 2
        elif stat < 12:
            return 3
        else:
            return 4

    def InventoryWeight(self):
        w = 0
        for i in self.INVENTORY:
            w += i.weight
        return w
        
        