import pygame
from Map import Map
from Agent import Agent
from Pirate import Pirate
from Hint import Hint_Manager

WIN_WIDTH = 1000
WIN_HEIGHT = 680
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Treasure island")

class Game:
    def __init__(self, fin_path):
        global FONT
        self.import_game_data(fin_path)
        self.map = Map(self.W, self.H, self.board, self.R)
        self.pirate = Pirate(self.map, (self.Tx, self.Ty), self.r, self.f)
        self.agent = Agent(self.map)
        self.treasure_loc = (self.Tx, self.Ty)
        self.hint_manager = Hint_Manager(self.agent, self.pirate, self.treasure_loc, self.map)

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
            self.map.map[self.Tx][self.Ty].entity = 'T'
            if self.PREV_TURN == self.CUR_TURN:
                self.map.draw_map(WIN)
            else:
                hint = self.hint_manager.get_random_hint(self.CUR_TURN)
                print(hint.use_hint()[0])
                print(hint.is_verified())
                self.pirate.run(self.CUR_TURN)


                self.PREV_TURN = self.CUR_TURN
            
            #Track event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    self.CUR_TURN += 1