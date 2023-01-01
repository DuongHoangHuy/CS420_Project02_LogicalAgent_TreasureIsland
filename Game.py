import pygame
pygame.init()
import sys
from Map import Map
from Agent import Agent
from Pirate import Pirate
from Hint import Hint_Manager
from Log import Logger
from helpers.constant import WIN_H, WIN_W

WIN = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Treasure island")

class Game:
    def __init__(self, fin_path, fout_path):
        global FONT
        self.import_game_data(fin_path)
        self.map = Map(self.W, self.H, self.board, self.R)
        self.pirate = Pirate(self.map, (self.Tx, self.Ty), self.r, self.f)
        self.agent = Agent(self.map, self.pirate)
        self.treasure_loc = (self.Tx, self.Ty)
        self.hint_manager = Hint_Manager(self.agent, self.pirate, self.treasure_loc, self.map)
        self.logger = Logger(fout_path)
        self.CUR_TURN = 0
        self.is_gameover = False
        self.run = True
    
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
    
    def check_state(self, run):
        if not self.is_gameover:
            self.logger.recieve_message(run(self.CUR_TURN), self.CUR_TURN)
            if self.agent.found_treasure or self.pirate.found_treasure:
                self.is_gameover = True
    
    def exec(self):
        print('Loi export: ', self.CUR_TURN)
        self.logger.recieve_message(f'Game start\n> The pirate’s prison is going to reveal the at the beginning of the turn {self.pirate.turn_reveal}\n> The pirate is free at the beginning of the turn {self.pirate.turn_escape}', self.CUR_TURN)
        next_turn = False
        while self.run:
            if not self.is_gameover:
                self.map.map[self.Tx][self.Ty].entity = 'T'

                if next_turn:
                    self.logger.recieve_message(f'START TURN {self.CUR_TURN}', self.CUR_TURN)
                    hint = self.hint_manager.get_random_hint(self.CUR_TURN)
                    self.logger.recieve_message(hint.get_hint_message(), self.CUR_TURN)
                    self.logger.recieve_message(self.agent.add_to_hintlist(hint), self.CUR_TURN)
                    self.check_state(self.pirate.run)
                    self.check_state(self.agent.run)
                    self.logger.recieve_message(f'END TURN {self.CUR_TURN}', self.CUR_TURN)
                    next_turn = False

            self.map.draw_map(WIN)
            self.pirate.draw(WIN, self.CUR_TURN)
            self.agent.draw(WIN, self.CUR_TURN)
            self.logger.draw(self.CUR_TURN, WIN)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    # self.logger.export_log()

                if event.type == pygame.KEYDOWN and not self.is_gameover:
                    self.CUR_TURN += 1
                    next_turn = True
        pygame.quit()
        
                    