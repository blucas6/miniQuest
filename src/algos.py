import math
import random
from copy import deepcopy

from configs.config import *

def straightPath(st, end, grid):
    dir = ""
    if st == end:
        return ""
    # vertical
    if st[0] == end[0]:
        while st != end:
            if st[1] - end[1] > 0:
                dir = "up"
                st[1] -= 1
            else:
                st[1] += 1
                dir = "down"
            if grid[st[1]][st[0]] == 1:
                return ""
        return dir
    # horizontal
    elif st[1] == end[1]:
        while st != end:
            if st[0] - end[0] > 0:
                dir = "left"
                st[0] -= 1
            else:
                st[0] += 1
                dir = "right"
            if grid[st[1]][st[0]] == 1:
                return ""
        return dir
    else:
        return ""

# # Straight path test
# grid = [[0,0,0,0,0],
#         [0,1,0,0,0],
#         [0,0,0,0,0],
#         [0,0,0,0,0]]
# st = [0,1]
# end = [3,1]
# dir = straightPath(st, end, grid)
# if dir != "":
#     print(dir)
# else:
#     print("no path")

def drawline(grid, pos, end):
    dx = abs(pos[0] - end[0])
    dy = abs(pos[1] - end[1])
    s = 0.99 / (dx if dx > dy else dy)
    t = 0.0
    while t < 1.0:
        dx = round((1.0 - t) * pos[0] + t*end[0])
        dy = round((1.0 - t) * pos[1] + t*end[1])
        if grid[dy][dx] != 1:       # one means wall
            grid[dy][dx] = 2        # two means seen
        else:
            return
        t += s

def FOV(grid, pos):
    f = 0
    while f <= (2*math.pi):
        x = FOV_RANGE * math.cos(f) + pos[0]
        y = FOV_RANGE * math.sin(f) + pos[1]
        drawline(grid, pos, [x, y])
        f += FOV_RADIAN

# *** FOV TEST *** #
# grid is a surrounded grid
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

class Cell:
    def __init__(self):
        self.parent = [-1, -1]
        self.f = -1
        self.g = -1
        self.h = -1
        self.m = -1
        self.mdir = "none"
    
def isValid(point, width, height):
    if point[0] >= 0 and point[0] < width and point[1] >= 0 and point[1] < height:
        return True
    return False

def isUnblocked(point, grid, gridw, gridh):
    # 0 is open cell
    return isValid(point, gridw, gridh) and grid[point[1]][point[0]] == 0

def isDestination(pos, dest):
    return pos == dest

def calculateHValue(src, dest):
    return math.sqrt(((src[0] - dest[0])*(src[0] - dest[0])) + ((src[1] - dest[1])*(src[1] - dest[1])))

def tracePath(cellDetails, dest):
    path = []

    row = dest[1]
    col = dest[0]

    while True:
        path.append([col, row])
        next_node = cellDetails[row][col].parent
        row = next_node[1]
        col = next_node[0]

        if cellDetails[row][col].parent == next_node:
            break

    path.append([col, row])
    path.reverse()
    return path

def aStar(src, dest, gridw, gridh, grid, momentum=1.0):
    if not isValid(src, gridw, gridh):
        print("ERROR: Astar - invalid src")
        return -1
    
    if not isValid(dest, gridw, gridh):
        print("ERROR: Astar - invalid dest")
        return -1

    # if not isUnblocked(src, grid, gridw, gridh) or not isUnblocked(dest, grid, gridw, gridh):
    #     print("ERROR: Astar - src or dest blocked")
    #     return
    
    if isDestination(src, dest):
        print("NOTE: src at dest")
        return -1

    # closed list boolean 2d array showing that no cell is included
    closed_list = []
    for j in range(gridh):
        row = []
        for i in range(gridw):
            row.append(False)
        closed_list.append(row)

    # 2d array to hold cell info
    cellDetails = []
    for r in range(gridh):
        row = []
        for c in range(gridw):
            row.append(Cell())
        cellDetails.append(row)

    # starting node
    i = src[0]
    j = src[1]
    cellDetails[j][i].f = 0.0
    cellDetails[j][i].g = 0.0
    cellDetails[j][i].h = 0.0
    cellDetails[j][i].m = 0.0
    cellDetails[j][i].parent = [i, j]

    # open list [ f, [i,j] ]    f = g + h 
    # add starting cell
    open_list = []
    open_list.append([0.0, [i, j]])

    while open_list:
        # find min f value
        p = open_list.pop(open_list.index(min(open_list)))
        i = p[1][0]
        j = p[1][1]

        closed_list[j][i] = True

        # gen successors
        for addx in range(-1, 2, 1):
            for addy in range(-1, 2, 1):
                if (addx==0 and addy==-1) or (addx==1 and addy==0) or (addx==0 and addy==1) or (addx==-1 and addy==0):
                    neighbour = [i + addx, j + addy]
                    # check if valid
                    if isValid(neighbour, gridw, gridh):
                        # check if dest
                        if isDestination(neighbour, dest):
                            cellDetails[neighbour[1]][neighbour[0]].parent = [i, j]
                            return tracePath(cellDetails, dest)
                            
                        # check if on closed list or blocked
                        elif not closed_list[neighbour[1]][neighbour[0]] and isUnblocked(neighbour, grid, gridw, gridh):
                            gnew = cellDetails[j][i].g + 1
                            hnew = calculateHValue(neighbour, dest)
                            fnew = gnew + hnew

                            # dir
                            if addx==0 and addy==-1:       #up
                                mdirNew = "top" 
                            elif addx==0 and addy==1:       #down
                                mdirNew = "down"
                            elif addx==1 and addy==0:       #right
                                mdirNew = "right"
                            elif addx==-1 and addy==0:       #left
                                mdirNew = "left"
                            if cellDetails[j][i].mdir == mdirNew:
                                mnew = cellDetails[j][i].m + momentum
                            else:
                                mnew = 0.0

                            # if not on open list add it and add info 
                            # or check if the cost is better
                            if cellDetails[neighbour[1]][neighbour[0]].f == -1 or cellDetails[neighbour[1]][neighbour[0]].f > fnew:
                                open_list.append([fnew, [neighbour[0],neighbour[1]]])
                                cellDetails[neighbour[1]][neighbour[0]].f = fnew
                                cellDetails[neighbour[1]][neighbour[0]].g = gnew
                                cellDetails[neighbour[1]][neighbour[0]].h = hnew
                                cellDetails[neighbour[1]][neighbour[0]].m = mnew
                                cellDetails[neighbour[1]][neighbour[0]].mdir = mdirNew
                                cellDetails[neighbour[1]][neighbour[0]].parent = [i, j]
    print("ERROR: Astar - failed to find path")
    grid[src[1]][src[0]] = "S"
    grid[dest[1]][dest[0]] = "D"
    for r in grid:
        print(r)
    return -1
    


def floodFill(xstart,ystart,start_color,color_to_update, matrix, width, height):
    #if the square is not the same color as the starting point
    if matrix[ystart][xstart] != start_color:
        return
    #if the square is not the new color
    elif matrix[ystart][xstart] == color_to_update:
        return
    else:
        #update the color of the current square to the replacement color
        matrix[ystart][xstart] = color_to_update
        neighbors = [(xstart-1,ystart),(xstart+1,ystart),(xstart-1,ystart-1),(xstart+1,ystart+1),(xstart-1,ystart+1),(xstart+1,ystart-1),(xstart,ystart-1),(xstart,ystart+1)]
        for n in neighbors:
            if 0 <= n[0] <= width-1 and 0 <= n[1] <= height-1:
                floodFill(n[0],n[1],start_color,color_to_update, matrix, width, height)

#  *** FLOOD FILL TEST *** #

# width = 10
# height = 20
# matrix = []
# for i in range(height):
#     row = []
#     for j in range(width):
#         row.append(0)
#     matrix.append(row)

# for r in range(random.randint(2, width)):
#     matrix[random.randint(0, height-1)][random.randint(0, width-1)] = "X"

# start_x = 0
# start_y = 0
# matrix[start_y][start_x] = 0
# for row in matrix:
#     print(row)

# print("-------------------")

# start_color = 0
# floodFill(start_x,start_y,start_color,2, matrix, width, height)

# for row in matrix:
#     print(row)


# *** A STAR TEST *** #

# gridtest = []
# w = 7
# h = 7
# for i in range(w):
#     row = []
#     for j in range(h):
#         row.append(0)
#     gridtest.append(row)

# src = [4,2]
# dest = [3, 6]
# for row in gridtest:
#     print(row)
# print("------------------------------")
# path = aStar(src, dest, w, h, gridtest)

# for p in path:
#     gridtest[p[1]][p[0]] = "+"

# gridtest[src[1]][src[0]] = "S"
# gridtest[dest[1]][dest[0]] = "E"

# for row in gridtest:
#     print(row)                                
                                







