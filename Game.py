import pygame
from Map import Map
from Pirate import Pirate

WIN_WIDTH = 1000
WIN_HEIGHT = 670
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Treasure island")

class Game:
    def __init__(self, fin_path):
        global FONT
        self.import_game_data(fin_path)
        self.map = Map(self.W, self.H, self.board)
        self.pirate = Pirate(self.map, (self.Tx, self.Ty), self.f)
        # self.gold_loc = (self.Tx, self.Ty)

        self.run = True
        self.PREV_TURN = 1
        self.CUR_TURN = 1
    
    def import_game_data(self, fin_path):
        f = open(fin_path, "r")
        size = f.readline().split()
        self.W = int(size[0])
        self.H = int(size[1])
        self.r = int(f.readline())
        self.f = int(f.readline())
        self.R = int(f.readline())
        treasure_loc = f.readline().split()
        self.Tx = int(treasure_loc[0])
        self.Ty = int(treasure_loc[1])
        self.board = []
        for line in f:
            lst_c = line.split(';')
            final = [c.strip() for c in lst_c]
            self.board.append(final)

        f.close()
    
    def exec(self):

        while self.run:
            if self.PREV_TURN == self.CUR_TURN:
                self.map.draw_map(WIN)
            else:
                self.pirate.run(self.CUR_TURN)


                self.PREV_TURN = self.CUR_TURN
            
            #Track event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    self.CUR_TURN += 1
        

if __name__ == "__main__":
    game = Game('sample_input.txt')
    game.exec()