import pygame

from config import *
from colors import *

class Menu:
    def __init__(self, game, w, h, offx, offy):
        self.game = game
        self.str_data = self.genString()
        self.width = w
        self.height = h
        self.offx = offx
        self.offy = offy
        self.contents = []
        self.resetContents()

    def Icon(self, game, coords, background, frontground):
        tile = game.TILESET.tiles[coords[0] * TILESET_AMOUNT_PER_ROW + coords[1]]
        icon = pygame.Surface((TILESET_W, TILESET_H))
        icon.blit(tile, (0,0))
        pxarray = pygame.PixelArray(icon)
        pxarray.replace(PIXEL_FG, frontground)
        pxarray.replace(PIXEL_BG, background)
        pxarray.close()
        return icon

    def resetContents(self):
        self.contents = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                img = self.Icon(self.game, [0,0], VOID, WHITE)
                row.append(img)
            self.contents.append(row)

    def loadStr(self):
        self.resetContents()
        self.str_data = self.genString()
        row = 0
        col = 0
        for c in range(len(self.str_data)):
            # print(row, col, self.height, self.width, self.str_data[c])
            if row > self.height:
                break
            if self.str_data[c] == "\n":
                col = -1
                row += 1
            elif self.str_data[c] != " ":
                coords = self.letterImg(self.str_data[c])
                img = self.Icon(self.game, coords, VOID, WHITE)
                self.contents[row][col] = img
            if col >= self.width:
                    row += 1
                    col = 0
            col += 1

    def letterImg(self, ch):
        # start at 2 on tilesheet
        r = 2
        c = 0
        for l in range(len(TYPING_STRING)):
            if TYPING_STRING[l] == "\n":
                r += 1
                c = -1
            elif TYPING_STRING[l] == ch:
                coords = [r,c]
                return coords
            c += 1
        
        print("ERROR: string formatting - not a supported character")
        coords = [0,0]
        return coords


class StatBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_STAT_W
        h = UI_STAT_H
        offx = 0
        offy = 1 + UI_MSG_H + 1 + 1 + MAP_H + 1
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        return "STR:%s DEX:%s LUCK:%s\nT:%s LV:%s H:%s" % (self.game.PLAYER.STR, self.game.PLAYER.DEX, self.game.PLAYER.LUCK, self.game.TURN, self.game.CURR_LEVEL+1, self.game.PLAYER.HEALTH)


class InfoBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_INFO_W
        h = UI_INFO_H
        offx = 1 + MAP_W + 1 + 1
        offy = 1 + UI_MSG_H + 1 + 1
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        return "%s\n\nArmor:\n\nMainH:\n\nAlt:\n\n" % (self.game.PLAYER.name)


class MessageBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_MSG_W
        h = UI_MSG_H
        offx = 1
        offy = 1
        self.MSG_STR = "Welcome to MiniQuest!"
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        return self.MSG_STR