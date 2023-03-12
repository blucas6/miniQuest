from entity import Entity
from properties import Property
from configs.icon_config import BLOOD_ICON
import colors

class Fluid(Entity):
    def __init__(self, game, pos, prop, icon, bg, fg, info, evap):
        self.EVAP = evap
        Entity.__init__(self, game, prop, icon, bg, fg, True, pos, info)
    
    def update(self):
        self.EVAP -= 1
        if self.EVAP < 0:
            self.game.CURRENT_LV_O.items.remove(self)

class Blood(Fluid):
    def __init__(self, game, pos):
        Fluid.__init__(self, game, pos, Property.BLOOD, BLOOD_ICON, colors.RED, colors.WHITE, "Blood", 10)