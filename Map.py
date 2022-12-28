import pygame
from Grid import Grid
from constant import MAP_H, MAP_W, GRID_H, GRID_W

WHITE = (255, 255, 255)
SILVER = (168, 169, 174)


class Map:
    def __init__(self, W, H, board, R):
        global GRID_W, GRID_H
        GRID_W = MAP_W // W
        GRID_H = MAP_H // H
        self.W = W
        self.H = H
        self.R = R
        self.map = self.make_map(W, H, board)
        self.FONT = pygame.font.SysFont('Arial', GRID_H-1)
        
    def make_map(self, W, H, board):
        grids = []
        for i in range(H):
            grids.append([])
            for j in range(W):
                w_grid = GRID_W
                h_grid = GRID_H
                grids[i].append(Grid(i, j, w_grid, h_grid, board[i][j]))

        return grids

    def reset_map(self):
        for row in range(self.H):
            for col in range(self.W):
                if self.map[row][col].is_masked:
                    self.map[row][col].is_masked = False
    
    def draw_map(self, WIN):
        WIN.fill(WHITE)

        for row in self.map:
            for grid in row:
                grid.draw(WIN, self.FONT)

        gap_row = GRID_W
        gap_col = GRID_H
        # number list
        for i in range(self.W):
            text = self.FONT.render(str(i), True, (0,0,0))
            center_rect = (gap_col*(i+1) + gap_col//2 - text.get_rect().width//2, 0)
            WIN.blit(text, center_rect)

        for i in range(self.H):
            text = self.FONT.render(str(i), True, (0,0,0))
            center_rect = (0, gap_row*(i+1) + gap_row//2 - text.get_rect().height//2)
            WIN.blit(text, center_rect)
            
        #Draw line
        for i in range(self.H+2):
            pygame.draw.line(WIN, SILVER, (0, i * gap_row), (GRID_W*(self.W+1), i * gap_row))
            for j in range(self.W+2):
                pygame.draw.line(WIN, SILVER, (j * gap_col, 0), (j * gap_col, GRID_H*(self.H+1)))

        # pygame.display.update()
