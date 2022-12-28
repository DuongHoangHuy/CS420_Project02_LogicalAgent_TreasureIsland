from queue import PriorityQueue
from copy import deepcopy
import random
import pygame
import math

DIRECTIONS = {(-1, 0): 'North', (1, 0): 'South', (0, 1): 'East', (0, -1): 'West'}

class Pirate:
    def __init__(self, map, treasure_loc, turn_reveal, turn_escape):
        self.map = map
        self.initial_loc = self.get_random_prison()
        self.current_loc = self.initial_loc #self.initialize_location()
        self.treasure_loc = treasure_loc
        self.turn_reveal = turn_reveal
        self.turn_escape = turn_escape # can bac 2
        self.path_instruction = self.astar() # A*

    def run(self, CUR_TURN):
        if CUR_TURN < self.turn_reveal:
            return ''
        if CUR_TURN == self.turn_reveal:
            return 'Pirate is in prison ' + str(self.initial_loc)
        if CUR_TURN < self.turn_escape:
            return ''
        if CUR_TURN == self.turn_escape:
            return 'Pirate is free'
        
        dest = self.path_instruction.pop()
        if self.current_loc is not self.initial_loc:
            self.map.map[self.current_loc[0]][self.current_loc[1]].entity = None
        self.map.map[dest[0]][dest[1]].entity = 'Pi'
        
        cor_x = dest[0] - self.current_loc[0]
        cor_y = dest[1] - self.current_loc[1]
        step = abs(cor_x) + abs(cor_y)
        if cor_x % 2 == 0:
            cor_x //= 2
        if cor_y % 2 == 0:
            cor_y //= 2

        direct = DIRECTIONS[(cor_x, cor_y)]
        self.current_loc = deepcopy(dest)
        return 'Pirate moves '+ str(step) + ' steps to the ' + direct

    
    def get_random_prison(self):
        prisons = []
        for row in self.map.map:
            for grid in row:
                if grid.entity == 'P':
                    prisons.append((grid.row, grid.col))
        
        return random.choice(prisons)
    
    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    def generate_neighbors(self, grid_loc):
        nbs = []
        for direct in DIRECTIONS:
            x = grid_loc[0] + direct[0]
            y = grid_loc[1] + direct[1]
            if x in range (0, self.map.W) and y in range (0, self.map.H):
                if self.map.map[x][y].is_barrier():
                    continue
                nbs.append((x, y))
            
            x = grid_loc[0] + 2*direct[0]
            y = grid_loc[1] + 2*direct[1]
            if x in range (0, self.map.W) and y in range (0, self.map.H) and (not self.map.map[x][y].is_barrier()):
                nbs.append((x, y))
        
        return nbs

    def reconstruct_path(self, came_from, current):
        path = [current]
        while came_from[current] is not self.initial_loc:
            path.append(came_from[current])
            current = came_from[current]
        return path

    def astar(self):
        cnt = 0
        open_set = PriorityQueue()
        open_set.put((0, cnt, self.initial_loc))
        came_from = {}
        g_score = {}
        g_score[self.initial_loc] = 0
        f_score = {}
        f_score[self.initial_loc] = self.h(self.initial_loc, self.treasure_loc)

        closed_set = []

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            closed_set.append(current)
            if current == self.treasure_loc:
                return self.reconstruct_path(came_from, current)

            neighbors = self.generate_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in closed_set:
                    cnt += 1
                    g_score[neighbor] = g_score[current] + 1
                    f_score[neighbor] = g_score[neighbor] + self.h(neighbor, self.treasure_loc)
                    open_set.put((f_score[neighbor], cnt, neighbor))
                    came_from[neighbor] = current

        return []


        
    

        