from config import *
from colors import *
from icon_config import *
from properties import Property

class Actor:
    def __init__(self, game, prop, col, icon, bg, fg, pos):
        self.game = game
        self.PROP = prop
        self.POS = pos
        self.isCOLL = col
        self.ICON = icon
        self.BG = bg
        self.FG = fg

    def update(self):
        pass

class Wasp(Actor):
    def __init__(self, game, pos):
        Actor.__init__(self, game, Property.WASP, True, WASP_ICON, VOID, YELLOW, pos)