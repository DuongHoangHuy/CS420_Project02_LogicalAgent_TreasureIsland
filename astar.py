import pygame
pygame.init()
from queue import PriorityQueue
from helpers.constant import DIRECTIONS

def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

def generate_neighbors(grid_loc, map, avai_step):
    nbs = []
    for direct in DIRECTIONS:
        for step in avai_step:
            x = grid_loc[0] + step*direct[0]
            y = grid_loc[1] + step*direct[1]
            if x in range (0, map.W) and y in range (0, map.H) and (not map.map[x][y].is_barrier()):
                nbs.append((x, y))
            else:
                break
    return nbs

def reconstruct_path(came_from, current, initial_loc):
    path = [current]
    while came_from[current] is not initial_loc:
        path.append(came_from[current])
        current = came_from[current]
    return path

def astar(initial_loc, treasure_loc, map, avai_step):
    if initial_loc == treasure_loc:
        return []
    cnt = 0
    open_set = PriorityQueue()
    open_set.put((0, cnt, initial_loc))
    came_from = {}
    g_score = {}
    g_score[initial_loc] = 0
    f_score = {}
    f_score[initial_loc] = h(initial_loc, treasure_loc)

    closed_set = []

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        closed_set.append(current)
        if current == treasure_loc:
            return reconstruct_path(came_from, current, initial_loc)

        neighbors = generate_neighbors(current, map, avai_step)
        for neighbor in neighbors:
            if neighbor not in closed_set:
                cnt += 1
                g_score[neighbor] = g_score[current] + 1
                f_score[neighbor] = g_score[neighbor] + h(neighbor, treasure_loc)
                open_set.put((f_score[neighbor], cnt, neighbor))
                came_from[neighbor] = current

    return []