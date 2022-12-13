from enum import Enum
import math

# class test(Enum):
#     A = 1
#     B = 2

# class thing:
#     def __init__(self, e):
#         self.info = e


# a = thing(test.A)
# b = thing(test.B)

# if a.info == b.info:
#     print(a.info)
# else:
#     print(a.info, b.info)

# print(test.A)

# def drawline(grid, pos, end):
#     dx = abs(pos[0] - end[0])
#     dy = abs(pos[1] - end[1])
#     s = 0.99 / (dx if dx > dy else dy)
#     t = 0.0
#     while t < 1.0:
#         dx = round((1.0 - t) * pos[0] + t*end[0])
#         dy = round((1.0 - t) * pos[1] + t*end[1])
#         if grid[dy][dx] != 1:
#             grid[dy][dx] = 2
#         else:
#             return
#         t += s

# def FOV(grid, pos):
#     f = 0
#     while f <= (2*math.pi):
#         x = FOV_RANGE * math.cos(f) + pos[0]
#         y = FOV_RANGE * math.sin(f) + pos[1]
#         drawline(grid, pos, [x, y])
#         f += FOV_RADIAN

# # *** FOV TEST *** #
# # grid is a surrounded grid
# grid = []
# w = 10
# h = 7
# for j in range(h):
#     row = []
#     for i in range(w):
#         if i == 0 or i == w-1 or j == 0 or j == h-1:
#             row.append(1)
#         else:
#             row.append(0)
#     grid.append(row)
# px = 5
# py = 3
# grid[3][5] = 9
# grid[2][6] = 1
# grid[2][7] = 1
# grid[4][2] = 1
# grid[5][3] = 1
# grid[3][3] = 1
# for r in grid:
#     print(r)
# FOV(grid, [px, py])
# print("---------------")
# grid[3][5] = 9
# for r in grid:
#     print(r)


# tmp = []
# for h in range(SCREEN_H):
#     row = []
#     for w in range(SCREEN_W):
#         row.append([])
#     tmp.append(row)

# for r in tmp:
#     print(r)

# tmp[1][4] = "c"

# print("--------------------------------------")
# for r in tmp:
#     print(r)

def weird(a):
    if a == 1:
        return True
    else:
        return 5
    
print(weird(1))
print(weird(9))
