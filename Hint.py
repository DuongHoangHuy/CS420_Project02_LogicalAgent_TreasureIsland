import random

# Tất cả hint trả về tile có chứa treasure

class Hint:
    def __init__(self, func):
        self.message = None
        self.tiles = None
        self.func = func

    def verify(self):
        res = self.func()
        

class Hint_Manager:
    def __init__(self, agent, pirate, map, W, H):
        self.agent = agent
        self.pirate = pirate
        self.map = map
        self.hints = [self.hint_1]
        self.W = W
        self.H = H

    def get_hint(self):
        return self.hints.pop(0)
    
    def hint_shuffle(self):
        pass 
        # hints = [(message, hint_1)]

    



    def hint_1(self):
        random_quantity = random.randrange(1, 12)
        tiles = []
        while len(tiles) < random_quantity:
            tile = (random.randrange(0, self.H), random.randrange(0, self.W))
            if tile not in tiles:
                tiles.append(tile)
        message = str(tiles) + " doesn't contain the treasure"
        return (message, tiles)
    
    def hint_2(self):
        return True
    
    def hint_1(self):
        return True
    
    def hint_1(self):
        return True

        