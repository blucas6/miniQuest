from time import sleep
import pygame

from colors import *
from config import *
from tileset import *
from level import *
from player import *
from menu import *
from display import Display

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        # self.clock = pygame.time.Clock()
        self.playing = False
        self.TURN = 0

        # tileset
        self.TILESET = Tileset(TILESET_FILE, [TILESIZE,TILESIZE], 0, 0)

        # PLAYER
        self.PLAYER = Player(self)

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
        self.MENUS = [MessageBar(self), StatBar(self), InfoBar(self)]

    def newLevel(self):
        # Create new level and add it to the level list
        # make current level the new level
        new_l = Level(self, self.CURR_LEVEL+1)
        self.LEVELS.append(new_l)

    def main(self):
        # game loop
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
        self.CURRENT_LV_O.clearLightMap()

        # PLAYER FOV 
        self.PLAYER.FOVsight(self.CURRENT_LV_O)

        # UPDATE entities and check if they are being ACTIVATED
        for e in self.LEVELS[self.CURR_LEVEL].items:
            if self.PLAYER.POS == e.POS and not e.activated:
                e.ACTIVATE()
            e.update()

        # UPDATE MENUS
        for m in self.MENUS:
            m.loadStr()

        # UPDATE LEVEL MAP
        self.CURRENT_LV_O.update()
    
    def events(self):
        rec_event = False
        while not rec_event:
            # sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    rec_event = True
                if event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    if event.key == pygame.K_q and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                        self.playing = False
                        rec_event = True
                    if event.key == pygame.K_LEFT:
                        if self.PLAYER.move([-1, 0]):
                            rec_event = True
                    if event.key == pygame.K_RIGHT:
                        if self.PLAYER.move([1, 0]):
                            rec_event = True
                    if event.key == pygame.K_UP:
                        if self.PLAYER.move([0, -1]):
                            rec_event = True
                    if event.key == pygame.K_DOWN:
                        if self.PLAYER.move([0, 1]):
                            rec_event = True
                    if event.key == pygame.K_COMMA and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                        if self.PLAYER.stairs("up"):
                            rec_event = True
                    if event.key == pygame.K_PERIOD and (mods & pygame.KMOD_LSHIFT or mods & pygame.KMOD_RSHIFT):
                        if self.PLAYER.stairs("down"):
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
            self.MENUS[0].MSG_STR = "You walk up the stairs"
        elif dir == "down":
            # GO DOWN - level pointer back one
            self.CURR_LEVEL -= 1
            print("go down")
            self.MENUS[0].MSG_STR = "You descend down"
        
        self.CURRENT_LV_O = self.LEVELS[self.CURR_LEVEL]

