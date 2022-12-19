import pygame
import math

from configs.config import *
from colors import *

class Menu:
    def __init__(self, game, w, h, offx, offy):
        self.game = game
        self.width = w
        self.height = h
        self.str_data = self.genString()
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
        if ch == " ":
            return [0,0]
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


class HealthBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_HEALTHBAR_W
        h = UI_HEALTHBAR_H
        offx = 1 + MAP_W + 1
        offy = 1 + UI_MSG_H + 1
        Menu.__init__(self, game, w, h, offx, offy)
    
    def genString(self):
        give_str = "[" + self.game.PLAYER.name + " " + str(round(self.game.PLAYER.CURR_HEALTH)) + "/" + str(round(self.game.PLAYER.HEALTH))
        give_str += (" "*(self.width - len(give_str)-1)) + "]"
        return give_str

    def loadStr(self):
        self.resetContents()
        self.str_data = self.genString()
        row = 0
        col = 0
        hp_boxes = round((self.width-2) * self.game.PLAYER.CURR_HEALTH / self.game.PLAYER.HEALTH)
        for c in range(len(self.str_data)):
            # print(row, col, self.height, self.width, self.str_data[c])
            if row > self.height:
                break
            if self.str_data[c] == "\n":
                col = -1
                row += 1
            else:
                if c < hp_boxes+1 and c != 0:
                    bg = GREEN
                    if self.game.PLAYER.CURR_HEALTH / self.game.PLAYER.HEALTH <= 0.1:
                        bg = RED
                    elif self.game.PLAYER.CURR_HEALTH / self.game.PLAYER.HEALTH <= 0.5:
                        bg = ORANGE
                else:
                    bg = VOID
                coords = self.letterImg(self.str_data[c])
                img = self.Icon(self.game, coords, bg, WHITE)
                self.contents[row][col] = img
            if col >= self.width:
                    row += 1
                    col = 0
            col += 1

class StatBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_STAT_W
        h = UI_STAT_H
        offx = 0
        offy = 1 + UI_MSG_H + 1 + 1 + MAP_H + 1
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        return "STR:%s DEX:%s LUCK:%s\nT:%s LV:%s" % (self.game.PLAYER.STR, self.game.PLAYER.DEX, self.game.PLAYER.LUCK, self.game.TURN, self.game.CURR_LEVEL+1)


class InfoBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_INFO_W
        h = UI_INFO_H
        offx = 1 + MAP_W + 1 + 1
        offy = 1 + UI_MSG_H + 1 + UI_HEALTHBAR_H + 1
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        armor = ""
        main = ""
        alt = ""
        if self.game.PLAYER.ARMOR != "":
            armor = self.game.PLAYER.ARMOR.name
        if self.game.PLAYER.MAIN_HAND != "":
            main = self.game.PLAYER.MAIN_HAND.name
        if self.game.PLAYER.ALT_HAND != "":
            alt = self.game.PLAYER.ALT_HAND.name
        return "Armor:%s\nMainH:%s\nAlt:%s" % (armor, main, alt)


class MessageBar(Menu):
    def __init__(self, game):
        self.game = game
        w = UI_MSG_W
        h = UI_MSG_H
        offx = 1
        offy = 1
        self.MSG_STR = ["","","Welcome to MiniQuest!"]
        Menu.__init__(self, game, w, h, offx, offy)

    def genString(self):
        give_str = ">" + self.MSG_STR[-1] + "\n" + self.MSG_STR[-2] + "\n" + self.MSG_STR[-3]
        return give_str

    def loadStr(self):
        self.resetContents()
        self.str_data = self.genString()
        row = 0
        col = 0
        grey_scale = 0
        for c in range(len(self.str_data)):
            # print(row, col, self.height, self.width, self.str_data[c])
            if row > self.height:
                break
            if self.str_data[c] == "\n":
                col = -1
                row += 1
                grey_scale += 1
            elif self.str_data[c] != " ":
                coords = self.letterImg(self.str_data[c])
                if grey_scale == 0:
                    fg = WHITE
                elif grey_scale == 1:
                    fg = LIGHT_GRAY
                else:
                    fg = GRAY
                img = self.Icon(self.game, coords, VOID, fg)
                self.contents[row][col] = img
            if col >= self.width:
                    row += 1
                    col = 0
            col += 1