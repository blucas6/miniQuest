import random as rand


from configs.config import *
from colors import *
from configs.icon_config import *
from properties import Property, Tag
from entity import LightMode
from configs.enemy_config import *
from algos import aStar, calculateHValue

class Actor:
    def __init__(self, game, prop, col, icon, bg, fg, pos, t_dist, a_range, speed, ac, hb, a_speed, hp, tag):
        self.game = game
        self.PROP = prop
        self.TAG = tag
        self.POS = pos
        self.isCOLL = col
        self.ICON = icon
        self.BG = bg
        self.FG = fg
        self.MODE = LightMode.UNSEEN

        # Stats
        self.HEALTH = hp
        self.ENERGY = 0
        self.SPEED = speed                  # how much energy to move
        self.AC = ac
        self.HitBonus = hb
        self.ATTACK_SPEED = a_speed         # how much energy to attack
        self.attack_range = a_range
        self.tracking_distance = t_dist     # not implemented

    def update(self, e):
        # add energy
        self.ENERGY += e
        while self.ENERGY > 0:
            action = False

            # first try for attack, can only attack once
            if self.attack():
                break

            # try for move towards player
            if self.move():
                action = True

            # if no actions could be completed end turn
            if not action:
                break

    def move(self):
        if self.ENERGY >= self.SPEED:
            self.game.CURRENT_LV_O.generateAstarPathfinding()
            path = aStar(self.POS, self.game.PLAYER.POS, MAP_W, MAP_H, self.game.CURRENT_LV_O.pathfinding_astar)
            if path == -1 or len(path) == 1:
                return False
            self.POS[0] = path[1][0]
            self.POS[1] = path[1][1]
            self.ENERGY -= self.SPEED
            return True
        return False
    
    def attack(self):
        if calculateHValue(self.POS, self.game.PLAYER.POS) <= self.attack_range and self.ENERGY >= self.ATTACK_SPEED:
            roll = rand.randint(0, 20)
            damage = self.getDmg_Melee()
            if roll == 20:
                damage += self.getDmg_Melee()
                self.game.PLAYER.takeRawDmg(damage)
            roll += self.HitBonus
            self.game.PLAYER.takeDmg(roll, damage)
            self.ENERGY -= self.ATTACK_SPEED
            return True
        return False

    def takeDmg(self, d):
        self.HEALTH -= d
        if self.HEALTH <= 0:
            self.game.CURRENT_LV_O.creatures.remove(self)
    
    def getDmg_Melee(self):
        print("ENEMY DEALS NO DAMAGE")
        return 0

class Wasp(Actor):
    def __init__(self, game, pos):
        Actor.__init__(self, game, Property.WASP, True, WASP_ICON, VOID, YELLOW, pos, WASP_TRACKING_DISTANCE, MELEE_ATTACK_RANGE, NORMAL_SPEED, WASP_AC, WASP_HITBONUS, NORMAL_SPEED, WASP_HP, Tag.ENEMY)
    
    def getDmg_Melee(self):
        # 1d1
        return 1


class Goblin_Scout(Actor):
    def __init__(self, game, pos):
        Actor.__init__(self, game, Property.GOBLIN_SCOUT, True, GOBLIN_ICON, VOID, GREEN, pos, GOBLIN_TRACKING_DISTANCE, MELEE_ATTACK_RANGE, NORMAL_SPEED, GOBLIN_AC, GOBLIN_HITBONUS, NORMAL_SPEED, GOBLIN_HP, Tag.ENEMY)

    def getDmg_Melee(self):
        # 1d2
        return rand.randint(1,2)