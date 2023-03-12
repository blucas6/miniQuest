import random as rand
from copy import deepcopy
import time

from configs.config import *
from colors import *
from configs.icon_config import *
from properties import Property, Tag
from entity import LightMode
from configs.enemy_config import *
from algos import aStar, calculateHValue, straightPath
from items import *
from fluid import Blood

class Actor:
    def __init__(self, game, prop, col, icon, bg, fg, pos, t_dist, a_range, speed, ac, mb, rb, a_speed, hp, tag):
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
        self.MeleeBonus = mb
        self.RangedBonus = rb
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
                self.ENERGY -= self.ATTACK_SPEED
                break

            # try for move towards player
            if self.move():
                self.ENERGY -= self.SPEED
                action = True

            # if no actions could be completed end turn
            if not action:
                break

    def move(self, movesInMomentum=0):
        if self.ENERGY >= self.SPEED:
            self.game.CURRENT_LV_O.generateAstarPathfinding()
            path = aStar(self.POS, self.game.PLAYER.POS, MAP_W, MAP_H, self.game.CURRENT_LV_O.pathfinding_astar, movesInMomentum)
            if path == -1 or len(path) == 1:
                return False
            self.POS[0] = path[1][0]
            self.POS[1] = path[1][1]
            return True
        return False

    def SendAttack(self, isMelee):
        roll = rand.randint(0,20)
        damage = 0
        if isMelee:
            damage = self.getDmg_Melee()
        else:
            damage = self.getDmg_Ranged()
        if roll == 20:
            if isMelee:
                damage += self.getDmg_Melee()
                self.game.PLAYER.takeRawDmg(damage)
            else:
                damage += self.getDmg_Ranged()
                self.game.PLAYER.takeRawDmg(damage)
            print("Monster Sent:", damage, " damage | roll:", roll)
        if isMelee:
            roll += self.MeleeBonus
        else:
            roll += self.RangedBonus
        print("Monster Sent:", damage, " damage | roll:", roll)
        self.game.PLAYER.takeDmg(roll, damage)

    
    def attack(self):
        if calculateHValue(self.POS, self.game.PLAYER.POS) <= self.attack_range and self.ENERGY >= self.ATTACK_SPEED:
            self.SendAttack(True)
            return True
        return False
    
    def triggerBlood(self):
        if rand.randint(1,2) == 1:
            x = self.POS[0] + rand.randint(-1, 1)
            y = self.POS[1] + rand.randint(-1, 1)
            print("CREATED BLOOD [%s,%s]" % (x,y))
            self.game.CURRENT_LV_O.fluids.append(Blood(self.game, [x,y]))

    def takeDmg(self, d):
        self.HEALTH -= d
        if self.HEALTH <= 0:
            self.game.CURRENT_LV_O.creatures.remove(self)
        self.triggerBlood()
    
    def getDmg_Melee(self):
        print("ENEMY DEALS NO MELEE DAMAGE")
        return 0

    def getDmg_Ranged(self):
        print("ENEMY DEALS NO RANGED DAMAGE")
        return 0

    def attack_ranged(self, launcher=None):
        self.game.CURRENT_LV_O.generateAstarPathfinding()
        # see if a straight path to target exists
        st = deepcopy(self.POS)
        end = deepcopy(self.game.PLAYER.POS)
        dir = straightPath(st, end, self.game.CURRENT_LV_O.pathfinding_astar)
        if dir != "":
            # if path exists fire
            st = deepcopy(self.POS)
            if launcher != None:
                if len(launcher.Bullets) > 0:
                    shot_projectile = launcher.Shoot(dir, self.game.CURRENT_LV_O, st)
                    for b in launcher.Bullets:
                        print(b.POS)
                else:
                    return False
            else:
                shot_projectile = self.Projectile
                shot_projectile.isShot(dir, self.game.CURRENT_LV_O, st)
            while shot_projectile.moving:
                shot_projectile.update()
                # hit player
                if shot_projectile.POS == self.game.PLAYER.POS:
                    self.SendAttack(False)
                    shot_projectile.moving = False
                self.game.CURRENT_LV_O.update()
                self.game.render()
                time.sleep(SHOT_PROJECTILE_SPEED)
            return True
        return False

class Wasp(Actor):
    def __init__(self, game, pos):
        Actor.__init__(self, game, Property.WASP, True, WASP_ICON, VOID, YELLOW, pos, WASP_TRACKING_DISTANCE, MELEE_ATTACK_RANGE, NORMAL_SPEED, WASP_AC, WASP_MELEE_BONUS, WASP_RANGED_BONUS, NORMAL_SPEED, WASP_HP, Tag.ENEMY)
    
    def getDmg_Melee(self):
        # 1d1
        return 1


class Goblin_Scout(Actor):
    def __init__(self, game, pos):
        self.Weapon = BlowGun(game, pos)
        self.Projectile = Dart(game)
        self.Weapon.Load(10)
        self.MovesInMomentum = 3    # needed to make sure the scout shoot along straight paths
        Actor.__init__(self, game, Property.GOBLIN_SCOUT, True, GOBLIN_ICON, VOID, GREEN, pos, GOBLIN_TRACKING_DISTANCE, MELEE_ATTACK_RANGE, NORMAL_SPEED, GOBLIN_AC, GOBLIN_MELEE_BONUS, GOBLIN_RANGED_BONUS, NORMAL_SPEED, GOBLIN_HP, Tag.ENEMY)

    def getDmg_Melee(self):
        # 1d2
        return rand.randint(1,2)
    
    def getDmg_Ranged(self):
        self.Projectile.RangedDmg()
        return 1

    def update(self, e):
        # add energy
        self.ENERGY += e
        while self.ENERGY > 0:
            action = False

            # try for attack, can only attack once
            if self.attack():
                self.ENERGY -= self.ATTACK_SPEED
                break

            # try for a ranged shot
            if self.attack_ranged(self.Weapon):
                self.ENERGY -= self.ATTACK_SPEED
                break

            # try for move towards player
            if self.move():
                self.ENERGY -= self.SPEED
                action = True

            # if no actions could be completed end turn
            if not action:
                break