import pygame

from config import *
from colors import *
from entity import UI, LighMode
from icon_config import *

class Display:
    def __init__(self, g):
        self.game = g
        self.screen = self.loadScreen()     # screen will hold only 1 image per cell
        
        # offset from level map coords to screen coords
        # ui msg height and 2 borders, 1 border on the width
        self.offseth = UI_MSG_H + 2
        self.offsetw = 1

    def Icon(self, coords, background, frontground):
        tile = self.game.TILESET.tiles[coords[0] * TILESET_AMOUNT_PER_ROW + coords[1]]
        icon = pygame.Surface((TILESET_W, TILESET_H))
        icon.blit(tile, (0,0))
        pxarray = pygame.PixelArray(icon)
        pxarray.replace(PIXEL_FG, frontground)
        pxarray.replace(PIXEL_BG, background)
        pxarray.close()
        return icon

    def loadScreen(self):
        tmp = []
        for h in range(SCREEN_H):
            row = []
            for w in range(SCREEN_W):
                row.append('')
            tmp.append(row)
        return tmp

    def CreateUI(self):
        # CLEAR SCREEN ARRAY
        # fill with VOID images
        for r in range(len(self.screen)):
            for c in range(len(self.screen[0])):
                self.screen[r][c] = self.Icon([0,0], VOID, WHITE)

        # UI BORDERS
        self.addBorders()

    def addBorders(self):
        # UI MESSAGE BOX
        self.addBox(0, 0, MAP_W+2 + UI_INFO_W, UI_MSG_H) 
        # UI MAP BOX
        self.addBox(0, UI_MSG_H+1, MAP_W+2, UI_MSG_H + MAP_H+2)
        # UI INFO BOX
        self.addBox(MAP_W+2, UI_MSG_H+1, MAP_W+1 + UI_INFO_W, UI_MSG_H + UI_STAT_H + MAP_H+1)

    def addBox(self, stx, sty, boxw, boxh):
        for j in range(int(WIN_HEIGHT / TILESIZE)):
            for i in range(int(WIN_WIDTH / TILESIZE)):
                # horizontal
                if (j == sty or j == boxh) and (i < boxw and i > stx):
                    self.screen[j][i] = self.Icon(UI("h").ICON, UI_BG, UI_FG)
                # vertical
                if (i == stx or i == boxw) and (j < boxh and j > sty):
                    self.screen[j][i] = self.Icon(UI("v").ICON, UI_BG, UI_FG)
                # corners
                if j == sty and i == stx:
                    self.screen[j][i] = self.Icon(UI("tl").ICON, UI_BG, UI_FG)
                if j == sty and i == boxw:
                    self.screen[j][i] = self.Icon(UI("tr").ICON, UI_BG, UI_FG)
                if j == boxh and i == stx:
                    self.screen[j][i] = self.Icon(UI("bl").ICON, UI_BG, UI_FG)
                if j == boxh and i == boxw:
                    self.screen[j][i] = self.Icon(UI("br").ICON, UI_BG, UI_FG)

    def DisplayScreen(self, menus_list, level_o, player_o):
        self.CreateUI()

        # ADD MENUS TO SCREEN
        for m in menus_list:
            for row in range(m.height):
                for col in range(m.width):
                    # print(row + UI_MSG_H + MAP_H, col)
                    self.screen[row + m.offy][col + m.offx] = m.contents[row][col]

        # ADD LEVEL TO SCREEN
        # go through Level Map in LEVEL obj
        # print("================================")
        # for r in level_o.Tower_Map:
        #     print(r)
        # print("------------------------------")
        # for r in level_o.Level_Map:
        #     print(r)
        for row in range(level_o.levelh):
            for col in range(level_o.levelw):
                if not level_o.Level_Map[row][col]:
                    icon = level_o.Tower_Map[row][col].ICON
                    bg = level_o.Tower_Map[row][col].BG
                    fg = level_o.Tower_Map[row][col].FG
                else:
                    icon = level_o.Level_Map[row][col][0].ICON
                    bg = level_o.Level_Map[row][col][0].BG
                    fg = level_o.Level_Map[row][col][0].FG
                # check light mode
                if level_o.Light_Map[row][col] == LighMode.UNSEEN:
                    icon = T_FLOOR_UNSEEN
                elif level_o.Light_Map[row][col] == LighMode.LIT:
                    bg = ORANGE
                self.screen[row + self.offseth][col + self.offsetw] = self.Icon(icon, bg, fg)

        # ADD PLAYER TO SCREEN
        # add in offset because player coords are map coords not screen coords
        self.screen[player_o.POS[1] + self.offseth][player_o.POS[0] + self.offsetw] = self.Icon(player_o.ICON, player_o.BG, player_o.FG)


        return self.screen

