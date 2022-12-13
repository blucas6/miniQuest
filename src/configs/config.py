from colors import *

# TILESET
TILESET_FILE = "../tileset/ascii16x16.png"
TILESET_W = 16
TILESET_H = 16
TILESET_AMOUNT_PER_ROW = 16
PIXEL_BG = (0, 0, 0)                # can't make an icon with a black fg and white bg
PIXEL_FG = (255, 255, 255)              
TILESIZE = 16

# LEVELS
MAP_W = 20     # real dimensions
MAP_H = 15

# TOWER
CURVATURE = 3
# TORCH
TORCH_AMOUNT = 3 

# PLAYER
PLAYER_ST = [round(MAP_W/2), round(MAP_H/2)]
FOV_RANGE = 6
FOV_RADIAN = 0.05

PLAYER_ST_STRENGTH = 1
PLAYER_ST_DEX = 1
PLAYER_ST_LUCK = 5
PLAYER_ST_SPEED = 3
PLAYER_ST_HEALTH = 10


# UI
UI_STAT_W = MAP_W
UI_STAT_H = 2
UI_INFO_W = 15
UI_INFO_H = MAP_H + UI_STAT_H
UI_MSG_W = MAP_W + 1 + 1 + UI_INFO_W
UI_MSG_H = 3
UI_BG = VOID
UI_FG = WHITE


# SCREEN - in pixels
WIN_WIDTH = (1+UI_MSG_W+1) * TILESIZE      # 1 - buffer tile
WIN_HEIGHT = (1 + UI_MSG_H + 1 + 1 + MAP_H + 1 + UI_STAT_H) * TILESIZE  
# SCREEN - in tiles
SCREEN_W = round(WIN_WIDTH / TILESIZE)
SCREEN_H = round(WIN_HEIGHT / TILESIZE)
print("WINDOW - W:", SCREEN_W, "tiles")
print("WINDOW - H:", SCREEN_H, "tiles")



#                      #                     #                                            #
# [           [#],    [##],                 [#],                  [###],                [###]                            ]
#                                            #                                            #
T_PIECES = [ [[0,0]], [[0,0],[0,-1],[1,0]], [[0,0],[0,-1],[0,1]], [[0,0],[-1,0],[1,0]], [[0,0],[-1,0],[1,0],[0,-1],[0,1]] ]
NUM_TOWER_W_PIECES = 15



# letters / numbers / symbols
TYPING_STRING = " !\"#$%&'()*+,-./\n0123456789:;<=>?\n@ABCDEFGHIJKLMNO\nPQRSTUVWXYZ[\]^_\n`abcdefghijklmno\npqrstuvwxyz{!}"

