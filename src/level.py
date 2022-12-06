import random as rand
import copy

from colors import *
from config import *
from algos import *
from entity import *
from actor import *
from icon_config import *

class Level:
    def __init__(self, game, id):
        self.Lvl_ID = id
        self.game = game

        self.Light_Map = self.LoadBlankLevelMap()   # controls what light mode each tile has - unseen, seen, lit    
        self.Tower_Map = []                         # stores all floors and wall tiles
        self.Level_Map = self.LoadBlankLevelMap()   # conglamerate of items/creatures in one double array
        self.items = []
        self.creatures = []

        self.available_pts = []     # list of all available points in the tower (no walls)

        self.astarGrid = []         # prebuilt grid of 1s 0s for path calculating

        self.genMap()

    def clearLightMap(self):
        self.Light_Map = self.LoadBlankLevelMap()

    def update(self):
        # compile Level_Map array with all items and creatures
        for c in self.creatures:
            lm = self.Light_Map[c.POS[1]][c.POS[0]]
            if lm == LighMode.SEEN:
                c.MODE = LighMode.SEEN
            elif lm == LighMode.LIT:
                c.MODE = LighMode.LIT
            else:
                c.MODE = LighMode.UNSEEN
            self.Level_Map[c.POS[1]][c.POS[0]].append(c)
        for i in self.items:
            lm = self.Light_Map[i.POS[1]][i.POS[0]]
            if lm == LighMode.SEEN:
                i.MODE = LighMode.SEEN
                i.already_seen = True
            elif lm == LighMode.LIT:
                i.MODE = LighMode.LIT
            elif lm == LighMode.UNSEEN and not i.already_seen:
                i.MODE = LighMode.UNSEEN
            self.Level_Map[i.POS[1]][i.POS[0]].append(i)

    def LoadBlankLevelMap(self):
        m = []
        for h in range(MAP_H):
            row = []
            for w in range(MAP_W):
                row.append([])
            m.append(row)
        return m
    
    def ResetLightMap(self):
        for h in range(MAP_H):
            for w in range(MAP_W):
                self.Light_Map[h][w].append(LighMode.UNSEEN)

    def genMap(self):
        self.ResetLightMap()
        self.buildAstarGrid()

        self.genTower()
        self.addStairs()
        self.genWalls()
        self.addTorches()
        self.addCreatures()

        # for row in self.astarGrid:
        #     print(row)

        self.update()

    def buildAstarGrid(self):
        # need wall pts
        for y in range(MAP_H):
            row = []
            for x in range(MAP_W):
                row.append(0)
            self.astarGrid.append(row)


    def genTower(self):     # generates the outside walls of the tower and the floor
        # create wall pts

        # TOWER WALLS
        for y in range(MAP_H):
            row = []
            for x in range(MAP_W):
                # top n bot
                if (y == 0 or y == MAP_H-1) and x > CURVATURE and x < MAP_W-1 - CURVATURE:
                    row.append(Wall(self.game, "h", [x,y]))
                    self.astarGrid[y][x] = 1
                # right n left
                elif (x == 0 or x == MAP_W-1) and y > CURVATURE and y < MAP_H-1 - CURVATURE:
                    row.append(Wall(self.game, "v", [x,y]))
                    self.astarGrid[y][x] = 1
                else:
                    row.append(Void(self.game, [x,y]))
            self.Tower_Map.append(row)

        # TOWER CURVES
        # create grid for astar
        grid = []
        for r in range(MAP_H):
            row = []
            for c in range(MAP_W):
                row.append(0)
            grid.append(row)

        # for r in grid:
        #     print(r)
        # add corners
        c_points = [[0, CURVATURE], [CURVATURE, 0], [CURVATURE, MAP_H-1], [0, MAP_H-1 - CURVATURE]]
        for c in range(0, 4, 2):
            # print(c_points[c], c_points[c+1], MAP_W, MAP_H)
            path = aStar(c_points[c], c_points[c+1], MAP_W, MAP_H, grid)
            # calculate symmetric path across horiz
            path_sym = []
            for p in path:
                self.Tower_Map[p[1]][p[0]] = Wall(self.game, "c", p)
                self.astarGrid[p[1]][p[0]] = 1
                path_sym.append([MAP_W-1 - p[0], p[1]])
            for p in path_sym:
                self.Tower_Map[p[1]][p[0]] = Wall(self.game, "c", p)
                self.astarGrid[p[1]][p[0]] = 1

        # TOWER FLOOR
        # pick middle of map and flood fill floor
        # create grid for flood fill
        grid = []
        for y in range(MAP_H):
            row = []
            for x in range(MAP_W):
                row.append(0)
            grid.append(row)
        for i in range(MAP_H):
            for j in range(MAP_W):
                if self.Tower_Map[i][j].PROP == Property.WALL:
                    grid[i][j] = 1

        floodFill(round((MAP_W-1)/2), round((MAP_H-1)/2), 0, 2, grid, MAP_W-1, MAP_H-1)

        # create available pts list
        for j in range(MAP_H):
            for i in range(MAP_W):
                if grid[j][i] == 2:
                    self.Tower_Map[j][i] = Floor(self.game, [i,j])
                    # add pts to list for later use
                    self.available_pts.append([i,j])

    def genWalls(self):     # generates the walls within the tower
        for a in range(NUM_TOWER_W_PIECES):
            c = rand.randint(0, len(self.available_pts)-1)
            spot = self.available_pts[c]
            p = rand.randint(0, len(T_PIECES)-1)
            piece = T_PIECES[p]
            for s in piece:
                if self.inBounds(s[0]+spot[0], s[1]+spot[1]) and self.available_pts.count([(spot[0] + s[0]), (spot[1] + s[1])]) > 0:
                    self.Tower_Map[spot[1] + s[1]][spot[0] + s[0]] = WallPiece(self.game, [(s[0]+spot[0]), (s[1]+spot[1])])
                    self.available_pts.remove([(spot[0] + s[0]), (spot[1] + s[1])])
                    self.astarGrid[spot[1] + s[1]][spot[0] + s[0]] = 1

    def addStairs(self):
        if self.Lvl_ID == 1:    # no downstairs on level 1
            s = rand.randint(0, len(self.available_pts)-1)
            self.items.append(Stair(self.game, "up", self.available_pts[s]))
            self.available_pts.remove(self.available_pts[s])
        else:
            # add downstair where player is standing
            dwn = copy.deepcopy(self.game.PLAYER.POS)
            self.items.append(Stair(self.game, "down", dwn))
            # print("added stair", dwn)
            self.available_pts.remove(dwn)
            # add upstair somewhere
            s = rand.randint(0, len(self.available_pts)-1)
            self.items.append(Stair(self.game, "up", self.available_pts[s]))
            self.available_pts.remove(self.available_pts[s])

    def addTorches(self):
        a = rand.randint(0, TORCH_AMOUNT)
        for t in range(a):
            s = rand.randint(0, len(self.available_pts)-1)
            self.items.append(Torch(self.game, self.available_pts[s]))
            self.available_pts.remove(self.available_pts[s])

    def addCreatures(self):
        print("current level gen:", self.Lvl_ID)
        amount = rand.randint(1, 5)
        for c in range(amount):
            s = rand.randint(0, len(self.available_pts)-1)
            self.creatures.append(Wasp(self.game, self.available_pts[s]))
            self.available_pts.remove(self.available_pts[s])

    def inBounds(self, x, y):
        if x < MAP_W and y < MAP_H and x >= 0 and y >= 0:
            return True
        return False

    def isWall(self, x, y):
        if self.Tower_Map[y][x].PROP == Property.WALL or self.Tower_Map[y][x].PROP == Property.WALL_PIECE or self.Tower_Map[y][x].PROP == Property.NOTHING:
            return True
        return False
