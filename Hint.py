import random
import numpy
import math
from helpers.constant import REGIONS, DIRECTIONS
# Viết 2 hàm:
# get_hint_(number): Trả về (message, data)
# data là dữ liệu cần dùng để sử dụng để verify_hint
# vd: 2-5 regions that 1 of them has the treasure -> data = (2,8,3) region 2, 8, 3
# A large rectangle area that has the treasure -> data = tọa độ (top, left, bottom, right)
# A column and/or a row that contain the treasure (rare) -> data = (random column/row number)

# verify_hint_(number): dùng data của hàm trên trả về để xử lí 
# -> make_massked() vùng ko có treasure
 
class Hint:
    def __init__(self, ID, get_hint, verify_hint):
        self.ID = None
        self.name = None
        self.message = None
        self.data = None
        self.verify_hint = verify_hint
        self.get_hint = get_hint
    
    def read_hint(self,  cur_turn):
        res = self.get_hint()
        self.name = f'Hint {cur_turn}'
        self.message = res[0]
        self.data = res[1]

    def is_verified(self):
        return self.verify_hint(self.data)
    
    def get_hint_message(self):
        return self.name + ': ' + self.message


class Hint_Manager:
    def __init__(self, agent, pirate, treasure_loc, map):
        self.agent = agent
        self.pirate = pirate
        self.treasure_loc = treasure_loc # tuple (row, col)
        self.map = map #self.map.map = 2D list of Grids
        self.map.Hints = [  Hint(1, self.get_hint_1, self.verify_hint_1),
                            Hint(2, self.get_hint_2, self.verify_hint_2),
                            Hint(3, self.get_hint_3, self.verify_hint_3),
                            Hint(4, self.get_hint_4, self.verify_hint_4),
                            Hint(5, self.get_hint_5, self.verify_hint_5),
                            Hint(6, self.get_hint_6, self.verify_hint_6),
                            Hint(7, self.get_hint_7, self.verify_hint_7),
                            Hint(8, self.get_hint_8, self.verify_hint_8),
                            Hint(9, self.get_hint_9, self.verify_hint_9),
                            Hint(10, self.get_hint_10, self.verify_hint_10),
                            Hint(11, self.get_hint_11, self.verify_hint_11),
                            Hint(12, self.get_hint_12, self.verify_hint_12),
                            Hint(13, self.get_hint_13, self.verify_hint_13),
                            Hint(14, self.get_hint_14, self.verify_hint_14),
                            Hint(15, self.get_hint_15, self.verify_hint_15) ]
        # self.map.Hints = [Hint(7, self.get_hint_3, self.verify_hint_3)] #TEST HINT

    def get_random_hint(self, cur_turn):
        hint = None
        res = None
        p_rare = 0.02
        num_of_rare = 2
        p_other = (1- num_of_rare*p_rare) / (15 - num_of_rare)
        p_lst = [p_other, p_other, p_other, p_other, p_other, p_other, p_rare, p_other, p_other, p_other, p_other, p_rare, p_other, p_rare, p_other]
        hint = random.choices(self.map.Hints, weights= p_lst, k = 1)[0]
        hint.read_hint(cur_turn)
        if cur_turn == 1:
            res = hint.is_verified()
            while not res:
                hint = random.choice(self.map.Hints)
                hint.read_hint(cur_turn)
                res = hint.is_verified()
            self.map.reset_map()
        return hint
    
    #HINT 1
    def get_hint_1(self):
        random_quantity = random.randrange(1, 13)
        tiles = []
        while len(tiles) < random_quantity:
            tile = (random.randrange(0, self.map.H), random.randrange(0, self.map.W))
            if tile not in tiles:
                tiles.append(tile)
        message = str(tiles) + " doesn't contain the treasure"
        return (message, tiles)
    
    def verify_hint_1(self, data):
        if self.treasure_loc in data:
            for row in range(self.map.H):
                for col in range(self.map.W):
                    if (row, col) not in data:
                        self.map.map[row][col].make_masked()

            return False

        for loc in data:
            self.map.map[loc[0]][loc[1]].make_masked()
        return True

    #HINT 2: 2-5 regions that 1 of them has the treasure.
    def get_hint_2(self):
        random_num = random.randint(2, 5)
        random_regions = random.choices(range(1, self.map.R), k = random_num)
        message = f'{random_regions} that 1 of them has the treasure'
        return (message, random_regions)

    def verify_hint_2(self, data):
        random_regions =  data
        t_row, t_col = self.treasure_loc
        t_region = self.map.map[t_row][t_col].region
        if t_region in random_regions:
            for row in range(self.map.H):
                for col in range(self.map.W):
                    if self.map.map[row][col].region not in random_regions:
                        self.map.map[row][col].make_masked()
            return True

        for row in range(self.map.H):
            for col in range(self.map.W):
                if self.map.map[row][col].region in random_regions:
                    self.map.map[row][col].make_masked()
        return False
    
    # HINT 3: 1-3 regions that do not contain the treasure.
    def get_hint_3(self):
        random_num = random.randint(1, 3)
        random_regions = random.choices(range(1, self.map.R), k = random_num)
        message = f'Regions {random_regions} do not contain the treasure'
        return (message, random_regions)

    def verify_hint_3(self, data):
        random_regions =  data
        t_row, t_col = self.treasure_loc
        t_region = self.map.map[t_row][t_col].region
        if t_region in random_regions:
            for row in range(self.map.H):
                for col in range(self.map.W):
                    if self.map.map[row][col].region not in random_regions:
                        self.map.map[row][col].make_masked()
            return False

        for row in range(self.map.H):
            for col in range(self.map.W):
                if self.map.map[row][col].region in random_regions:
                    self.map.map[row][col].make_masked()
        return True

    #HINT 4: A large rectangle area that has the treasure.
    def get_hint_4(self):
        size = size = self.map.H // 4
        random_loc = (random.randint(0, self.map.H-size-1), random.randint(0, self.map.W-size-1))
        message = f'A large rectangle area {random_loc[0], random_loc[1], random_loc[0] + size, random_loc[1] + size} that has the treasure'
        return ( message, (random_loc[0], random_loc[1], random_loc[0] + size, random_loc[1] + size))
        
    def verify_hint_4(self, data):
        top, left, bot, right = data
        if self.treasure_loc[0] in range(top, bot+1) and self.treasure_loc[1] in range(left, right+1):
            for row in range(self.map.H):
                for col in range(self.map.W):
                    if row not in range(top, bot+1) or col not in range(left, right+1):
                        self.map.map[row][col].make_masked()
            return True
        for row in range(top, bot+1):
            for col in range(left, right+1):
                self.map.map[row][col].make_masked()
        return False

    #HINT 5: A small rectangle area that doesn't has the treasure.
    def get_hint_5(self):
        size = self.map.H // 8
        random_loc = (random.randint(0, self.map.H-size-1), random.randint(0, self.map.W-size-1))
        message = f'A small rectangle area {random_loc[0], random_loc[1], random_loc[0] + size, random_loc[1] + size} that doesn not have the treasure'
        return ( message, (random_loc[0], random_loc[1], random_loc[0] + size, random_loc[1] + size))
        
    def verify_hint_5(self, data):
        top, left, bot, right = data
        if self.treasure_loc[0] in range(top, bot+1) and self.treasure_loc[1] in range(left, right+1):
            for row in range(self.map.H):
                for col in range(self.map.W):
                    if row not in range(top, bot+1) or col not in range(left, right+1):
                        self.map.map[row][col].make_masked()
            return False

        for row in range(top, bot+1):
            for col in range(left, right+1):
                self.map.map[row][col].make_masked()
        return True

    # HINT 6:He tells you that you are the nearest person to the treasure (between 
    #  you and the prison he is staying).
    def get_hint_6(self):
        message = "Agent is the nearest person to the treasure"
        return [message, None]
        
    def verify_hint_6(self, data):
        agent_distance = abs(self.agent.current_loc[0] - self.treasure_loc[0]) + abs(self.agent.current_loc[1] - self.treasure_loc[1])
        pirate_distance = abs(self.pirate.current_loc[0] - self.treasure_loc[0]) + abs(self.pirate.current_loc[1] - self.treasure_loc[1]) 
        res = False
        if agent_distance < pirate_distance:
            res = True
        for row in range(self.map.H):
            for col in range(self.map.W):
                dist_from_agent = abs(self.agent.current_loc[0] - row) + abs(self.agent.current_loc[1] - col)
                dist_from_pirate = abs(self.pirate.current_loc[0] - row) + abs(self.pirate.current_loc[1] - col) 
                if res and dist_from_agent >= dist_from_pirate:
                    self.map.map[row][col].make_masked()
                elif not res and dist_from_pirate > dist_from_agent:
                    self.map.map[row][col].make_masked()

        return res

    # HINT 7: A column and/or a row that contain the treasure (rare).
    def get_hint_7(self):
        row, col = (random.randrange(0, self.map.H), random.randrange(0, self.map.W))
        choose = random.choice([0, 1, 2])
        if choose == 0:
            message = f'Row {row} contains the treasure'
        elif choose == 1:
            message = f'Column {col} contains the treasure'
        else:
            message = f'Row {row} and column {col} contains the treasure'

        return (message, [choose, (row, col)])

    def verify_hint_7(self, data):
        choose = data[0]
        row, col = data[1]

        grids = []
        if choose == 0 or choose == 2:
            for c in range(self.map.W):
                grids.append((row, c))

        if choose == 1 or choose == 2:
            for r in range(self.map.H):
                grids.append((r, col))
        
        if self.treasure_loc in grids:
            for r in range(self.map.H):
                for c in range(self.map.W):
                    if (r, c) not in grids:
                        self.map.map[r][c].make_masked()
            return True
        
        for grid in grids:
            self.map.map[grid[0]][grid[1]].make_masked()
        return False


    # HINT 8: A column and/or a row that do not contain the treasure.
    def get_hint_8(self):
        row, col = (random.randrange(0, self.map.H), random.randrange(0, self.map.W))
        choose = random.choice([0, 1, 2])
        if choose == 0:
            message = f'Row {row} does not contain the treasure'
        if choose == 1:
            message = f'Column {col} does not contain the treasure'
        else:
            message = f'Row {row} and column {col} do not contain the treasure'

        return (message, [choose, (row, col)])

    def verify_hint_8(self, data):
        choose = data[0]
        row, col = data[1]

        grids = []
        if choose == 0 or choose == 2:
            for c in range(self.map.W):
                grids.append((row, c))

        if choose == 1 or choose == 2:
            for r in range(self.map.H):
                grids.append((r, col))
        
        if self.treasure_loc in grids:
            for r in range(self.map.H):
                for c in range(self.map.W):
                    if (r, c) not in grids:
                        self.map.map[r][c].make_masked()
            return False
        
        for grid in grids:
            self.map.map[grid[0]][grid[1]].make_masked()
        return True
    
    #HINT 9
    def get_nb_regions(self):
        nb_regions = [[] for i in range(self.map.R-1)]
        for row in range(self.map.H):
            for col in range(self.map.W):
                cur_grid = self.map.map[row][col]
                if not cur_grid.is_sea():
                    for direct in DIRECTIONS:
                        nb_row = row + direct[0]
                        nb_col = col + direct[1]
                        if nb_row in range(self.map.H) and nb_col in range(self.map.W):
                            nb_region = self.map.map[nb_row][nb_col].region
                            cur_region = cur_grid.region
                            if nb_region is not cur_region and nb_region is not 0 and nb_region not in nb_regions[cur_region-1]:
                                nb_regions[cur_region-1].append(nb_region)
        
        return nb_regions

    def get_boundaries(self, region, nb_region):
        boundaries_loc = []
        for row in range(self.map.H):
            for col in range(self.map.W):
                grid = self.map.map[row][col]
                if grid.region == REGIONS[region]:
                    for direct in DIRECTIONS:
                        nb_row = row + direct[0]
                        nb_col = col + direct[1]
                        if nb_row in range(self.map.H) and nb_col in range(self.map.W) and self.map.map[nb_row][nb_col].region is REGIONS[nb_region]:
                            if (row, col) not in boundaries_loc:
                                boundaries_loc.append((row, col))
                            if (nb_row, nb_col) not in boundaries_loc:
                                boundaries_loc.append((nb_row, nb_col))
        
        return boundaries_loc

    def get_hint_9(self):
        nb_regions = self.get_nb_regions()
        region = random.randrange(1, self.map.R)
        nb_region = random.choice(nb_regions[region-1])
        message = "The treasure is somewhere in the boundary of region " + str(region) + ' and ' + str(nb_region)
        return [message, (region, nb_region)]
        
    def verify_hint_9(self, data):
        region, nb_region = data
        boundaries_loc = self.get_boundaries(region, nb_region)

        if self.treasure_loc not in boundaries_loc:
            for loc in boundaries_loc:
                self.map.map[loc[0]][loc[1]].make_masked()
            return False

        for row in range(self.map.H):
            for col in range(self.map.W):
                if (row, col) not in boundaries_loc:
                    self.map.map[row][col].make_masked()
        return False    
    
    #HINT 10
    def get_hint_10(self):
        message = 'The treasure is somewhere in a boundary of 2 regions'
        return [message, None]
        
    def verify_hint_10(self, data):
        nb_regions = self.get_nb_regions()
        boundaries_loc = []
        for region in range(len(nb_regions)):
            for nb_region in nb_regions[region]:
                boundary_loc = self.get_boundaries(region+1, nb_region)
                boundaries_loc.extend(boundary_loc)

        if self.treasure_loc not in boundaries_loc:
            for loc in boundaries_loc:
                self.map.map[loc[0]][loc[1]].make_masked()
            return False

        for row in range(self.map.H):
            for col in range(self.map.W):
                if (row, col) not in boundaries_loc:
                    self.map.map[row][col].make_masked()
        return True

    #HINT 11: The treasure is somewhere in an area bounded by 2-3 tiles from sea.
    def get_hint_11(self):
        distance = random.randint(2, 3)
        message = f'The treasure is somewhere in an area bounded by {distance} tiles from sea'
        return (message, distance)

    def verify_hint_11(self, data):
        distance = data
        grids = []
        for row in range(self.map.H):
            for col in range(self.map.W):
                if self.map.map[row][col].is_sea():
                    for direct in DIRECTIONS:
                        for i in range(1, distance+1):
                            nb_grid = (row + i*direct[0], col +  i*direct[1])
                            if nb_grid[0] in range(self.map.H) and nb_grid[1] in range(self.map.W) and not self.map.map[nb_grid[0]][nb_grid[1]].is_sea():
                                grids.append(nb_grid)

        if self.treasure_loc not in grids:
            for grid in grids:
                self.map.map[grid[0]][grid[1]].make_masked()
            return False
        
        for row in range(self.map.H):
            for col in range(self.map.W):
                if (row, col) not in grids:
                    self.map.map[row][col].make_masked()
        return True


    #HINT 12: A half of the map without treasure (rare).
    def get_hint_12(self):
        half_side = random.randint(0, 1)
        message = "Right" if half_side else "Left"
        message += " half does not contain the treasure"
        return (message, half_side)

    def verify_hint_12(self, data):
        if data == 0: 
            if self.treasure_loc[1] > (self.map.W // 2):
                for c in range(0, self.map.W // 2 + 1):
                    for r in range(0, self.map.H):
                        self.map.map[r][c].make_masked()
                return True
            else:
                for c in range(self.map.W // 2 + 1, self.map.W):
                    for r in range(0, self.map.H):
                        self.map.map[r][c].make_masked()

        if data == 1: 
            if self.treasure_loc[1] <= (self.map.W // 2): # #when equal?
                for c in range(self.map.W // 2 + 1, self.map.W):
                    for r in range(0, self.map.H):
                        self.map.map[r][c].make_masked()
                return True
            else:
                for c in range(0, self.map.W // 2 + 1):
                    for r in range(0, self.map.H):
                        self.map.map[r][c].make_masked()

        return False

    #HINT: 13
    def get_hint_13(self):
        direct = random.choice(['W', 'E', 'N', 'S', 'SE', 'SW', 'NE', 'NW'])

        message = 'From the prison ' + str(self.pirate.initial_loc) + ', the direction that has the treasure is ' + direct
        return (message, direct)

    def verify_hint_13(self, data):
        direct = data
        if direct in ['SE', 'SW', 'NE', 'NW']:
            row_range = range(0,0)
            col_range = range(0,0)
            if direct == 'SE':
                row_range = range(0, self.pirate.initial_loc[0] + 1)
                col_range = range(self.pirate.initial_loc[1], self.map.W)
            elif direct == 'SW':
                row_range =  range(0, self.pirate.initial_loc[0] + 1)
                col_range = range(0, self.pirate.initial_loc[1] + 1)
            elif direct == 'NE':
                row_range =  range(self.pirate.initial_loc[0], self.map.H)
                col_range = range(self.pirate.initial_loc[1], self.map.W)
            elif direct == 'NW':
                row_range =  range(self.pirate.initial_loc[0], self.map.H)
                col_range = range(0, self.pirate.initial_loc[1] + 1)

            if self.treasure_loc[0] not in row_range or self.treasure_loc[1] not in col_range:
                for row in row_range:
                    for col in col_range:
                        self.map.map[row][col].make_masked()
                return False

            for row in range(self.map.H):
                for col in range(self.map.W):
                    if row not in row_range or col not in col_range:
                        self.map.map[row][col].make_masked()
            return True

        elif direct in ['W', 'E', 'N', 'S']:
            f1 = None  #True is greater
            f2 = None
            if direct == 'E':
                f1 = 1
                f2 = 1
            elif direct == 'W':
                f1 = -1
                f2  = -1
            elif direct == 'N':
                f1 = 1
                f2 = -1
            elif direct == 'S':
                f1 = -1
                f2 = 1
            
            def func(cor, f1, f2, x, y):
                l1 = (y - cor[1]) - (x - cor[0])
                l2 = (y - cor[1]) + (x - cor[0])
                if l1*f1 >= 0 and l2*f2 >= 0:
                    return True
                return False
            
            if not func(self.pirate.initial_loc , f1, f2, self.treasure_loc[0], self.treasure_loc[1]):
                for r in range(self.map.H):
                    for c in range(self.map.W):
                        if func(self.pirate.initial_loc, f1, f2, r, c):
                            self.map.map[r][c].make_masked()
                return False

            for r in range(self.map.H):
                for c in range(self.map.W):
                    if not func(self.pirate.initial_loc, f1, f2, r, c):
                        self.map.map[r][c].make_masked()
            return True                    

    def get_hint_14(self):
        top_large, left_large, size_large = None, None, None
        SIZE_MIN = self.map.H // 4
        while True:
            top_large = random.randrange(0, self.map.H)
            left_large = random.randrange(0, self.map.W)
            size_large = random.randrange(SIZE_MIN, self.map.W)
            if top_large + size_large < self.map.H and left_large + size_large < self.map.W:
                break
        
        top_small, left_small, size_small = None, None, None
        while True:
            top_small = random.randrange(top_large+1, top_large + size_large)
            left_small = random.randrange(left_large+1, left_large + size_large)
            size_small = random.randrange(1, size_large)
            if top_small + size_small < top_large + size_large and left_small + size_small < left_large + size_large:
                break
        
        cor_large = [top_large, left_large, top_large + size_large, left_large + size_large]
        cor_small = [top_small, left_small, top_small + size_small, left_small + size_small]
        message = 'The treasure is somewhere inside the gap between 2 squares (top, left, bottom, right) ' + str(cor_large) + ' and ' + str(cor_small)
        return (message, (cor_large, cor_small))

    def verify_hint_14(self, data):
        cor_large, cor_small = data
        t_row, t_col = self.treasure_loc
        if t_row in range(cor_large[0], cor_large[2] + 1) and t_col in range(cor_large[1], cor_large[3]+1) and not (t_row in range(cor_small[0], cor_small[2] + 1) and t_col in range(cor_small[1], cor_small[3]+1)):
            for row in range(0, self.map.H):
                for col in range(0, self.map.W):
                    if row in range(cor_large[0], cor_large[2] + 1) and col in range(cor_large[1], cor_large[3]+1) and not (row in range(cor_small[0], cor_small[2] + 1) and col in range(cor_small[1], cor_small[3]+1)):
                        continue
                    self.map.map[row][col].make_masked()
            return True

        for row in range(0, self.map.H):
            for col in range(0, self.map.W):
                if row in range(cor_large[0], cor_large[2] + 1) and col in range(cor_large[1], cor_large[3]+1) and not (row in range(cor_small[0], cor_small[2] + 1) and col in range(cor_small[1], cor_small[3]+1)):
                    self.map.map[row][col].make_masked()
        return False

    def get_hint_15(self):
        message = 'The treasure is in a region that has mountain'
        return [message, None]

    def verify_hint_15(self, data):
        regions = [False for i in range(self.map.R)]
        for row in range(0, self.map.H):
            for col in range(0, self.map.W):
                if self.map.map[row][col].is_mountain():
                    regions[self.map.map[row][col].region-1] = True
        
        t_region = self.map.map[self.treasure_loc[0]][self.treasure_loc[1]].region
        if regions[t_region-1]:
            for row in range(0, self.map.H):
                for col in range(0, self.map.W):
                    if not self.map.map[row][col].is_sea() and not regions[self.map.map[row][col].region-1]:
                        self.map.map[row][col].make_masked()
            return True
        
        for row in range(0, self.map.H):
            for col in range(0, self.map.W):
                if not self.map.map[row][col].is_sea() and regions[self.map.map[row][col].region-1]:
                    self.map.map[row][col].make_masked()
        return False
                    

    # def get_hint_number(self):
    # def verify_hint_number(self, data):
