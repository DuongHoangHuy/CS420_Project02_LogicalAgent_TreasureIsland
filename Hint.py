import random
import numpy

# Viết 2 hàm:
# get_hint_(number): Trả về (message, data)
# data là dữ liệu cần dùng để sử dụng để verify_hint
# vd: 2-5 regions that 1 of them has the treasure -> data = (2,8,3) region 2, 8, 3
# A large rectangle area that has the treasure -> data = tọa độ (top, left, bottom, right)
# A column and/or a row that contain the treasure (rare) -> data = (random column/row number)

# verify_hint_(number): dùng data của hàm trên trả về để xử lí 
# -> make_massked() vùng ko có treasure
 
class Hint:
    def __init__(self, get_hint, verify_hint):
        self.message = None
        self.data = None
        self.verify_hint = verify_hint
        self.get_hint = get_hint
    
    def use_hint(self):
        res = self.get_hint()
        self.message = res[0]
        self.data = res[1]
        return res

    def is_verified(self, map):
        return self.verify_hint(self.data, map)

class Hint_Manager:
    def __init__(self, agent, pirate, treasure_loc, map, W, H):
        self.agent = agent
        self.pirate = pirate
        self.treasure_loc = treasure_loc # tuple (row, col)
        self.map = map # map.map = 2D list of Grids
        self.W = W # number of column (map)
        self.H = H # number of rows (map)
        self.hints = [Hint(self.get_hint_1, self.verify_hint_1)] # Chua can

    def get_random_hint(self):
        return random.choice(self.hints)

    # HINT 1: A list of random tiles that doesn't contain the treasure (1 to 12).
    def get_hint_1(self):
        random_quantity = random.randrange(1, 12) #(1, 13) ?
        tiles = []
        while len(tiles) < random_quantity: 
            tile = (random.randrange(0, self.H), random.randrange(0, self.W))
            if tile not in tiles:
                tiles.append(tile)
        message = str(tiles) + " doesn't contain the treasure"
        return (message, tiles)
    
    def verify_hint_1(self, data, map):
        if self.treasure_loc in data:
            return False

        # Mask
        for loc in data:
            map.map[loc[0]][loc[1]].make_masked() 
        return True

    # HINT 7: A column and/or a row that contain the treasure (rare).
    # distribution: col = row = 0.45, both = 0.1
    def get_hint_7(self):
        loc = (0, 0)
        while loc == (0, 0):
            loc = (random.randrange(0, self.H + 1), random.randrange(0, self.W + 1))

        choose = numpy.random.choice(numpy.arange(0, 3), p=[0.45, 0.45, 0.1])
        if choose == 0:
            message = "Row " + str(loc[0]) + " contains the treasure"
        if choose == 1:
            message = "Col " + str(loc[1]) + " contains the treasure"
        else:
            message = "Tile " + str(loc) + " contains the treasure"
        loc += (choose, -1)

        return (message, loc)

    def verify_hint_7(self, data, map):
        if data[2] == 0: # row only
            # mask
            if self.treasure_loc[0] == data[0]:
                for r in range(0, self.H):
                    if r != data[0]:
                        for c in range(0, self.W):
                            map.map[r][c].make_masked()
                return True
            else:
                for c in range(0, self.W):
                    map.map[data[0]][c].make_masked()

        if data[2] == 1: # col only
            if self.treasure_loc[1] == data[1]:
                for c in range(0, self.W):
                    if c != data[1]:
                        for r in range(0, self.H):
                            map.map[r][c].make_masked()
                return True
            else:
                for r in range(0, self.H):
                            map.map[r][data[1]].make_masked()

        if data[2] == 2: # both 
            if self.treasure_loc[0] == data[0] and self.treasure_loc[1] == data[1]:
                for r in range(0, self.W):
                    for c in range(0, self.H):
                        if (r,c) != self.treasure_loc:
                            map.map[r][c].make_masked()
                return True
            else:
                map.map[data[0]][data[1]].make_masked()

        return False


    # HINT 8: A column and/or a row that do not contain the treasure.
    # distribution: col = row = 0.25, both = 0.5
    def get_hint_8(self):
        loc = (0, 0)
        while loc == (0, 0):
            loc = (random.randrange(0, self.H + 1), random.randrange(0, self.W + 1))
        choose = numpy.random.choice(numpy.arange(0, 3), p=[0.25, 0.25, 0.5])
        if choose == 0:
            message = "Row " + str(loc[0]) + " does not contain the treasure"
        if choose == 1:
            message = "Col " + str(loc[1]) + " does not contain the treasure"
        else:
            message = "Tile " + str(loc) + " does not contain the treasure"
        loc += (choose, -1)
        return (message, loc)

    def verify_hint_8(self, data, map):
        if data[2] == 0: # row only
            # mask
            if self.treasure_loc[0] != data[0]:
                for c in range(0, self.W):
                    map.map[data[0]][c].make_masked()
                return True
            else:
                for r in range(0, self.H):
                    if r != data[0]:
                        for c in range(0, self.W):
                            map.map[r][c].make_masked()

        if data[2] == 1: # col only
            if self.treasure_loc[1] != data[1]:
                for r in range(0, self.H):
                    map.map[r][data[1]].make_masked()
                return True
            else:
                for c in range(0, self.W):
                    if c != data[1]:
                        for r in range(0, self.H):
                            map.map[r][c].make_masked()

        if data[2] == 2: # both 
            if self.treasure_loc[0] != data[0] and self.treasure_loc[1] != data[1]:
                map.map[data[0]][data[1]].make_masked()
                return True
            else:
                for r in range(0, self.W):
                    for c in range(0, self.H):
                        if (r,c) != self.treasure_loc:
                            map.map[r][c].make_masked()

        return False


    #HINT 11: The treasure is somewhere in an area bounded by 2-3 tiles from sea.
    def get_hint_11(self):
        quantity = random.randint(2, 3)
        message = "The treasure is somewhere in an area bounded by " + str(quantity) + " tiles from sea"
        return (message, quantity)

    def verify_hint_12(self, data, map):
        frontier = []
        for r in range(0, self.W):
            for c in range(0, self.H):
                if map.map[r + data][c + data].region == SEA or map.map[r + data][c - data].region == SEA or map.map[r - data][c + data].region == SEA or map.map[r - data][c - data].region == SEA and map.map[r][c].region != SEA:
                    frontier.append((r, c))
        if self.treasure_loc in frontier:
            for r in range(0, self.W):
                for c in range(0, self.H):
                    if (r, c) not in frontier:
                        map.map[r][c].make_masked()
            return True

        for item in frontier:
            map.map[item[0]][item[1]].make_masked()
        return False

    #HINT 12: A half of the map without treasure (rare).
    def get_hint_12(self):
        half_side = random.randint(0, 1)
        message = "Right" if half_side else "Left"
        message += " half does not contain the treasure"
        return (message, half_side)

    def verify_hint_12(self, data, map):
        if data == 0: 
            if self.treasure_loc[1] > (self.W // 2):
                for c in range(0, self.W // 2 + 1):
                    for r in range(0, self.H):
                        map.map[r][c].make_masked()
                return True
            else:
                for c in range(self.W // 2 + 1, self.W):
                    for r in range(0, self.H):
                        map.map[r][c].make_masked()

        if data == 1: 
            if self.treasure_loc[1] <= (self.W // 2): # #when equal?
                for c in range(self.W // 2 + 1, self.W):
                    for r in range(0, self.H):
                        map.map[r][c].make_masked()
                return True
            else:
                for c in range(0, self.W // 2 + 1):
                    for r in range(0, self.H):
                        map.map[r][c].make_masked()

        return False

        