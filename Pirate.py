from copy import deepcopy
import random
from helpers.constant import DIRECTIONS
from astar import astar

class Pirate:
    def __init__(self, map, treasure_loc, turn_reveal, turn_escape):
        self.map = map
        self.initial_loc = self.get_random_prison()
        self.current_loc = self.initial_loc #self.initialize_location()
        self.treasure_loc = treasure_loc
        self.turn_reveal = turn_reveal
        self.turn_escape = turn_escape # can bac 2
        self.path_instruction = astar(self.initial_loc, self.treasure_loc, self.map, [1, 2]) # A*
        self.found_treasure = False
        self.current_direct = None

    def run(self, CUR_TURN):
        if CUR_TURN < self.turn_reveal:
            return ''
        if CUR_TURN == self.turn_reveal:
            return 'Pirate is in prison ' + str(self.initial_loc)
        if CUR_TURN < self.turn_escape:
            return ''
        message = ''
        if CUR_TURN == self.turn_escape:
            message += 'Pirate is free/'
        
        dest = self.path_instruction.pop()
        cor_x = dest[0] - self.current_loc[0]
        cor_y = dest[1] - self.current_loc[1]
        step = abs(cor_x) + abs(cor_y)
        if cor_x % 2 == 0:
            cor_x //= 2
        if cor_y % 2 == 0:
            cor_y //= 2

        self.current_direct = DIRECTIONS[(cor_x, cor_y)]
        self.current_loc = deepcopy(dest)
        message +=  f'Pirate moves {step} steps to the {self.current_direct}'
        if not len(self.path_instruction):
            self.found_treasure = True
            message += '/Pirate found the treasure, Pirate won!'
        
        return message

    def get_current_direct(self):
        return self.current_direct

    
    def get_random_prison(self):
        prisons = []
        for row in self.map.map:
            for grid in row:
                if grid.entity == 'P':
                    prisons.append((grid.row, grid.col))
        
        return random.choice(prisons)
    
    def draw(self, win, cur_turn):
        if cur_turn < self.turn_escape:
            return
        PIRATE =  (215, 227, 86) #PIRATE
        x = (self.current_loc[1] + 3/2) * self.map.grid_w
        y = (self.current_loc[0] + 3/2)* self.map.grid_h
        text = self.map.FONT.render('Pi', True, PIRATE)
        center_rect = (x - text.get_rect().width/2, y - text.get_rect().height/2)
        win.blit(text, center_rect)

        