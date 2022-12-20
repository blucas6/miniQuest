import pygame

from colors import *
from configs.config import *
from tileset import *
from level import *
from player import *
from menu import *
from display import Display
from configs.message_config import *
from properties import Context

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # self.clock = pygame.time.Clock()
        self.playing = False
        self.TURN = 0
        self.CONTEXT = Context.DEFAULT

        # tileset
        self.TILESET = Tileset(TILESET_FILE, [TILESIZE,TILESIZE], 0, 0)

        # PLAYER
        self.PLAYER = Player(self)
        self.ADD_ENERGY = 0

        # screen array to hold all image tiles
        self.screen_tiles = []
        self.sw = WIN_WIDTH / TILESIZE
        self.sh = WIN_HEIGHT / TILESIZE

        self.Displayer = Display(self)
    
    def newGame(self):
        self.playing = True

        if not self.sw.is_integer() or not self.sh.is_integer():
            self.playing = False
            print("ERROR: Bounds are not integers check TILESIZE - screen")
            return

        self.CURR_LEVEL = 0
        self.LEVELS = [Level(self, 1)]
        self.CURRENT_LV_O = self.LEVELS[self.CURR_LEVEL]

        # MENUS
        self.MENUS = [MessageBar(self), StatBar(self), InfoBar(self), HealthBar(self)]

    def newLevel(self):
        # Create new level and add it to the level list
        # make current level the new level
        new_l = Level(self, self.CURR_LEVEL+1)
        self.LEVELS.append(new_l)

    def main(self):
        # game loop
        self.PLAYER.update()
        self.update()
        self.render()
        pygame.display.update()
        while self.playing:
            self.TURN += 1
            self.events()
            self.update()
            self.render()
            pygame.display.update()
            # print("TURN:", self.TURN)
            # self.clock.tick(60)

    def update(self):
        if self.CONTEXT == Context.DEFAULT:
            # UPDATE PLAYER - player action, light map generated from FOV
            self.PLAYER.update()

            # UPDATE entities and check if they are being ACTIVATED
            for i in self.LEVELS[self.CURR_LEVEL].items:
                if self.PLAYER.POS == i.POS and not i.activated:
                    i.ACTIVATE()
                i.update()
            
            # UPDATE creatures and add energy
            for c in self.CURRENT_LV_O.creatures:
                c.update(self.ADD_ENERGY)
            # reset energy back to 0, wait for new energy from player
            self.ADD_ENERGY = 0

            # UPDATE MENUS
            for m in self.MENUS:
                m.update() 

            # UPDATE LEVEL MAP - create composite level array 
            self.CURRENT_LV_O.update()

        elif self.CONTEXT == Context.MESSAGES:
            for m in self.MENUS:
                m.update()
    
    def events(self):
        rec_event = False
        while not rec_event:
            # sleep(0.1)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.playing = False
                    rec_event = True
                if event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_q and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                            self.playing = False
                            rec_event = True
                    if self.CONTEXT == Context.DEFAULT:
                        if event.key == pygame.K_LEFT:
                            turns = self.PLAYER.move([-1, 0])
                            if turns != -1:
                                self.ADD_ENERGY = turns
                                rec_event = True
                                break
                        elif event.key == pygame.K_RIGHT:
                            turns = self.PLAYER.move([1, 0])
                            if turns != -1:
                                self.ADD_ENERGY = turns
                                rec_event = True
                                break
                        elif event.key == pygame.K_UP:
                            turns = self.PLAYER.move([0, -1])
                            if turns != -1:
                                self.ADD_ENERGY = turns
                                rec_event = True
                                break
                        elif event.key == pygame.K_DOWN:
                            turns = self.PLAYER.move([0, 1])
                            if turns != -1:
                                self.ADD_ENERGY = turns
                                rec_event = True
                                break
                        elif event.key == pygame.K_COMMA and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                            if self.PLAYER.stairs("up"):
                                rec_event = True
                        elif event.key == pygame.K_PERIOD and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                            if self.PLAYER.stairs("down"):
                                rec_event = True
                    elif self.CONTEXT == Context.MESSAGES:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
                            self.MENUS[0].IncrementIndex()
                            rec_event = True

    def render(self):
        self.screen_tiles = self.Displayer.DisplayScreen(self.MENUS, self.LEVELS[self.CURR_LEVEL], self.PLAYER)
        # BLIT SCREEN ARRAY
        for row in range(len(self.screen_tiles)):
            for col in range(len(self.screen_tiles[0])):
                self.window.blit(self.screen_tiles[row][col], (col*TILESIZE, row*TILESIZE))


    def changeLevel(self, dir):
        if dir == "up":
            # GO UP - check if there is an above level first
            # or create new level and append to level list
            self.CURR_LEVEL += 1
            if len(self.LEVELS)-1 == self.CURR_LEVEL-1:       # if we were already at highest level then make new level
                self.newLevel()
            print("go up")   
            self.NewMessage(GO_UP_STAIR_MSG)
        elif dir == "down":
            # GO DOWN - level pointer back one
            self.CURR_LEVEL -= 1
            print("go down")
            self.NewMessage(GO_DOWN_STAIR_MSG)
        
        self.CURRENT_LV_O = self.LEVELS[self.CURR_LEVEL]

    def NewMessage(self, msg):
        self.MENUS[0].MSG_STR.append(msg)

    def SetContext(self, context):
        self.CONTEXT = context

