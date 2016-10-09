import pygame
from textrect import render_textrect
from enum import Enum

class Color(Enum):
    blue = pygame.Color('#0076CE')
    orange = pygame.Color('#E85719')
    red = pygame.Color('#AF0505')
    white = pygame.Color('#FFFFFF')
    yellow = pygame.Color('#F2C605')
    green = pygame.Color('#4BAE03')
    black = pygame.Color('#000000')

class Display:
    def __init__(self):
        pygame.display.init()
        pygame.mouse.set_visible(0)
        self.font_path = "../resources/fonts/Exo-SemiBold.ttf"
        self.big_font = pygame.font.Font(self.font_path, 96)
        self.font = pygame.font.Font(self.font_path, 48)
        self.info = pygame.display.Info()
        self.display = pygame.display.set_mode((self.info.current_w, self.info.current_h))

    def draw_label(self, text, rect, foreground, background, font):
        self.display.blit(render_textrect(text,
                                          font,
                                          pygame.Rect(0, 0, rect[2], rect[3]),
                                          foreground.value,
                                          background.value,
                                          justification=1),
                          (rect[0], rect[1]))

    def set_question(self, question, answers):
        width = self.info.current_w
        height = self.info.current_h
        self.draw_label(question, (0, 0, width, height * 0.6), Color.white, Color.black, self.big_font)
        self.draw_label(answers[0], (width / 3, height * 0.6, width / 3, height * 0.09), Color.black, Color.blue, self.font)
        self.draw_label(answers[1], (width / 3, height * 0.7, width / 3, height * 0.09), Color.black, Color.orange, self.font)
        self.draw_label(answers[2], (width / 3, height * 0.8, width / 3, height * 0.09), Color.black, Color.green, self.font)
        self.draw_label(answers[3], (width / 3, height * 0.9, width / 3, height * 0.09), Color.black, Color.yellow, self.font)

    def set_score(self, player_number, score):
        width = self.info.current_w
        height = self.info.current_h
        self.draw_label(str(score),
                        (0 if (player_number % 2) == 0 else (width / 3) * 2,
                         height * 0.6 if player_number > 1 else height * 0.8,
                         width / 3,
                         height * 0.2),
                        Color.white, Color.black, self.big_font)
