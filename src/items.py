
from properties import Property

class Item:
    def __init__(self, n, i_type):
        self.name = n
        self.PROP = i_type

class Armor(Item):
    def __init__(self, n, ac):
        i_type = Property.ARMOR
        self.ArmorClass = ac
        Item.__init__(self, n, i_type)

class Leather_Armor(Armor):
    def __init__(self):
        name = "Leather Armor"
        ac = 10
        Armor.__init__(self, name, ac)

class Sword(Item):
    def __init__(self, n, mthb, athb):
        i_type = Property.WEAPON
        self.MainToHit_Bonus = mthb
        self.AltToHit_Bonus = athb
        Item.__init__(self, n, i_type)

class Wooden_Sword(Sword):
    def __init__(self):
        n = "Wooden Sword"
        mthb = 0
        athb = 0
        Sword.__init__(self, n, mthb, athb)

    def getDmg(self):
        # 1d1
        return 1