import random

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

    def get_hint_1(self):
        random_quantity = random.randrange(1, 12)
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

    # def get_hint_number(self):

    # def verify_hint_number(self, data, map):

    # def get_hint_number(self):
    # def verify_hint_number(self, data, map):
