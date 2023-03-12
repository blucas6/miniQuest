import random as rand
import copy

from properties import Property
from entity import Entity
from configs.icon_config import *
from colors import *

class Weapon(Entity):
    def __init__(self, n, i_type, w, pos, game, icon, bg, fg, col, mthb, athb, ac, tb):
        self.WEIGHT = w
        self.MainToHitBonus = mthb
        self.AltToHitBonus = athb
        self.ArmorClass = ac 
        self.ThrownBonus = tb
        Entity.__init__(self, game, i_type, icon, bg, fg, col, pos, n)

    def update(self):
        print("ITEM DOES NOT UPDATE")

class Launcher(Weapon):
    def __init__(self, n, mthb, athb, tb, w, pos, ac, game, icon, bg, fg, col, proj_obj):
        i_type = Property.LAUNCHER
        self.Projectile = proj_obj
        self.Bullets = []
        Weapon.__init__(self, n, i_type, w, pos, game, icon, bg, fg, col, mthb, athb, ac, tb)

    def Load(self, load_num):
        for p in range(load_num):
            bul = copy.copy(self.Projectile)
            self.Bullets.append(bul)

class BlowGun(Launcher):
    def __init__(self, game, pos=[0,0]):
        name = "Blow Gun"
        icon = BLOWGUN_ICON
        bg = VOID
        fg = BROWN
        col = False
        main_to_hit_bonus = -3
        alt_to_hit_bonus = 0
        armor_class = 0
        thrown_bonus = -2
        weight = 1
        projectile = Dart(game)
        Launcher.__init__(self, name, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight, pos, armor_class, game, icon, bg, fg, col, projectile)

    def Shoot(self, dir, level_obj, pos):
        if self.Bullets:
            b = self.Bullets[0]
            b.isShot(dir, level_obj, pos)
            return self.Bullets.pop(0)

class Projectile(Weapon):
    def __init__(self, n, mthb, athb, tb, w, d, pos, ac, game, icon, bg, fg, col):
        i_type = Property.PROJECTILE
        self.goDir = d
        self.moving = False
        Weapon.__init__(self, n, i_type, w, pos, game, icon, bg, fg, col, mthb, athb, ac, tb)

    def isShot(self, dir, level_obj, pos):
        self.goDir = dir
        self.moving = True
        self.POS = pos
        level_obj.items.append(self)

    def update(self):
        next_pos = [0,0]
        if self.moving:
            if self.goDir == "right":
                next_pos = [1,0]
            elif self.goDir == "left":
                next_pos = [-1,0]
            elif self.goDir == "up":
                next_pos = [0,-1]
            elif self.goDir == "down":
                next_pos = [0,1]
            else:
                print("INCORRECT PROJECTILE DIRECTION!")
                self.moving = False
            new_pos = [self.POS[0] + next_pos[0], self.POS[1] + next_pos[1]]
            if self.game.CURRENT_LV_O.pathfinding_astar[new_pos[1]][new_pos[0]] == 1:
                self.moving = False
            else:
                self.POS = new_pos

class Dart(Projectile):
    def __init__(self, game, direction="", pos=[0,0]):
        name = "Pellet"
        icon = DART_ICON
        bg = VOID
        fg = BROWN
        col = False
        main_to_hit_bonus = -4
        alt_to_hit_bonus = -1
        armor_class = 0
        thrown_bonus = 1
        weight = 1
        Projectile.__init__(self, name, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight, direction, pos, armor_class, game, icon, bg, fg, col)

    def MeleeDmg(self):
        # 1d1
        return 1

    def RangedDmg(self):
        # 1d1
        return 1

class Armor(Weapon):
    def __init__(self, n, ac, mthb, athb, tb, w, pos, game, icon, bg, fg, col):
        i_type = Property.ARMOR
        Weapon.__init__(self, n, i_type, w, pos, game, icon, bg, fg, col, mthb, athb, ac, tb)

class Leather_Armor(Armor):
    def __init__(self, game, pos=[0,0]):
        name = "Leather Armor"
        icon = ARMOR_ICON
        bg = VOID
        fg = BROWN
        col = False
        ac = 1
        main_to_hit_bonus = -1
        alt_to_hit_bonus = -5
        thrown_bonus = -4
        weight = 25
        Armor.__init__(self, name, ac, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight, pos, game, icon, bg, fg, col)
    
    def MeleeDmg(self):
        # 1d1
        return 1
    
    def RangedDmg(self):
        # 1d1
        return 1

class Sword(Weapon):
    def __init__(self, n, mthb, athb, tb, w, pos, game, icon, bg, fg, col, ac):
        i_type = Property.WEAPON
        Weapon.__init__(self, n, i_type, w, pos, game, icon, bg, fg, col, mthb, athb, ac, tb)

class Wooden_Sword(Sword):
    def __init__(self, game, pos=[0,0]):
        n = "Wooden Sword"
        icon = SWORD_ICON
        bg = VOID
        fg = BROWN
        col = False
        main_to_hit_bonus = 0
        alt_to_hit_bonus = 0
        armor_class = 0
        thrown_bonus = -1
        weight = 5
        Sword.__init__(self, n, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight, pos, game, icon, bg, fg, col, armor_class)

    def MeleeDmg(self):
        # 1d2
        return rand.randint(1,2)
    
    def RangedDmg(self):
        # 1d1
        return 1

class Iron_Sword(Sword):
    def __init__(self, game, pos=[0,0]):
        n = "Iron Sword"
        icon = SWORD_ICON
        bg = VOID
        fg = GRAY
        col = False
        main_to_hit_bonus = 1
        alt_to_hit_bonus = 0
        armor_class = 0
        thrown_bonus = -2
        weight = 10
        Sword.__init__(self, n, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight, pos, game, icon, bg, fg, col, armor_class)

    def MeleeDmg(self):
        # 1d4
        return rand.randint(1,4)
    
    def RangedDmg(self):
        #1d1
        return 1