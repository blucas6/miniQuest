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

P_ST_STRENGTH = 1
P_ST_DEX = 1
P_ST_LUCK = 5


# UI
UI_MSG_H = 3
UI_INFO_W = 15
UI_STAT_H = 3
UI_BG = VOID
UI_FG = WHITE


# SCREEN - in pixels
WIN_WIDTH = (MAP_W+2 + UI_INFO_W + 1) * TILESIZE      # 1 - buffer tile
WIN_HEIGHT = (MAP_H+2 + UI_MSG_H + UI_STAT_H + 1) * TILESIZE  
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

