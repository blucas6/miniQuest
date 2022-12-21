import random as rand

from properties import Property

class Item:
    def __init__(self, n, i_type, w):
        self.name = n
        self.PROP = i_type
        self.WEIGHT = w

class Armor(Item):
    def __init__(self, n, ac, mthb, athb, tb, w):
        i_type = Property.ARMOR
        self.ArmorClass = ac            # How much BONUS armor it gives
        self.MainToHit_Bonus = mthb
        self.AltToHit_Bonus = athb
        self.ThrownBonus = tb
        Item.__init__(self, n, i_type, w)

class Leather_Armor(Armor):
    def __init__(self):
        name = "Leather Armor"
        ac = 1
        main_to_hit_bonus = -1
        alt_to_hit_bonus = -5
        thrown_bonus = -4
        weight = 25
        Armor.__init__(self, name, ac, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight)
    
    def MeleeDmg(self):
        # 1d1
        return 1
    
    def RangedDmg(self):
        # 1d1
        return 1

class Sword(Item):
    def __init__(self, n, mthb, athb, tb, w):
        i_type = Property.WEAPON
        self.MainToHit_Bonus = mthb     # How much BONUS to hit modifier it gives
        self.AltToHit_Bonus = athb      # May give off hand bonus
        self.ThrownBonus = tb
        self.ArmorClass = 0
        Item.__init__(self, n, i_type, w)

class Wooden_Sword(Sword):
    def __init__(self):
        n = "Wooden Sword"
        main_to_hit_bonus = 0
        alt_to_hit_bonus = 0
        thrown_bonus = -1
        weight = 5
        Sword.__init__(self, n, main_to_hit_bonus, alt_to_hit_bonus, thrown_bonus, weight)

    def MeleeDmg(self):
        # 1d2
        return rand.randint(1,2)
    
    def RangedDmg(self):
        # 1d1
        return 1