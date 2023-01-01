import pygame
pygame.init()
from Grid import Grid
from helpers.constant import MAP_H, MAP_W

WHITE = (255, 255, 255)
SILVER = (168, 169, 174)


class Map:
    def __init__(self, W, H, board, R):
        self.grid_w = MAP_W // W
        self.grid_h = MAP_H // H
        self.W = W
        self.H = H
        self.R = R
        self.map = self.make_map(W, H, board)
        self.FONT = pygame.font.SysFont('Arial', self.grid_h-1)
        self.prisons = self.get_all_prisons()
    
    def get_all_prisons(self):
        prisons = []
        for row in self.map:
            for grid in row:
                if grid.entity == 'P':
                    prisons.append((grid.row, grid.col))
        return prisons
        
    def make_map(self, W, H, board):
        grids = []
        for i in range(H):
            grids.append([])
            for j in range(W):
                grids[i].append(Grid(i, j, self.grid_w, self.grid_h, board[i][j]))

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

        gap_row = self.grid_w
        gap_col = self.grid_h

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
            pygame.draw.line(WIN, SILVER, (0, i * gap_row), (self.grid_w*(self.W+1), i * gap_row))
            for j in range(self.W+2):
                pygame.draw.line(WIN, SILVER, (j * gap_col, 0), (j * gap_col, self.grid_h*(self.H+1)))

        # pygame.display.update()
