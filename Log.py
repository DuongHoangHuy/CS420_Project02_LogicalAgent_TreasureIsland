import pygame
pygame.init()
from helpers.constant import WIN_W, WIN_H, MAP_H, MAP_W
from helpers.textrect import render_textrect

LOG_W = 400
LOG_H = 500
LOG_LINES = 10
LOG_COLOR = (222, 222, 222)

class Logger:
    def __init__(self, fout_path):
        self.messages = []
        self.area = pygame.Rect(MAP_W + (WIN_W - MAP_W - LOG_W)//2, (WIN_H - LOG_H)//3, LOG_W, LOG_H)
        self.font = pygame.font.SysFont('Arial', 12)
        self.fout_path = fout_path

    def export_log(self):
        f = open(self.fout_path, "w")
        for turn_log in self.messages:
            f.write(turn_log)
        print('Save logs successfully')
        f.close()

    def recieve_message(self, messages, cur_turn):
        # if not messages:
        #     return
        if cur_turn > len(self.messages)-1:
            self.messages.append('')
        splitted_messages = messages.split('/')
        for message in splitted_messages:
            self.messages[cur_turn] += '\n> ' + message

    def draw(self, cur_turn, win):
        rendered_text = render_textrect(self.messages[cur_turn], self.font, self.area, (0,0,0), LOG_COLOR)
        win.blit(rendered_text, self.area.topleft)