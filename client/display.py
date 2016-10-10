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
        for i in range(4):
            self.set_score(i, 0)

    def draw_label(self, text, rect, foreground, background, font):
        self.display.blit(render_textrect(text,
                                          font,
                                          pygame.Rect(0, 0, rect[2], rect[3]),
                                          foreground.value,
                                          background.value,
                                          justification=1),
                          (rect[0], rect[1]))

    def draw_answer(self, text, correct, rect, color):
        inverse = correct == None or text == correct
        self.draw_label(text,
                        rect,
                        Color.black if inverse else color,
                        color if inverse else Color.black,
                        self.font)

    def set_question(self, question, answers, correct=None):
        width = self.info.current_w
        height = self.info.current_h
        self.draw_label(question, (0, 0, width, height * 0.6), Color.white, Color.black, self.big_font)
        self.draw_answer(answers[0], correct, (width / 3, height * 0.6, width / 3, 70), Color.blue)
        self.draw_answer(answers[1], correct, (width / 3, height * 0.7, width / 3, 70), Color.orange)
        self.draw_answer(answers[2], correct, (width / 3, height * 0.8, width / 3, 70), Color.green)
        self.draw_answer(answers[3], correct, (width / 3, height * 0.9, width / 3, 70), Color.yellow)
        for player in range(4):
            self.set_player_answered_color(player, Color.black)

    def set_player_answered_color(self, player_number, color):
        width = self.info.current_w
        height = self.info.current_h
        x = int(80 if (player_number % 2) == 0 else width - 80)
        y = int(height * 0.67 if player_number > 1 else height * 0.87)
        pygame.draw.circle(self.display,
                           color.value,
                           (x, y),
                           48)

    def set_player_answered(self, player_number, correct):
        self.set_player_answered_color(player_number, (Color.green if correct else Color.red))

    def set_score(self, player_number, score):
        width = self.info.current_w
        height = self.info.current_h
        self.draw_label(str(score),
                        (0 if (player_number % 2) == 0 else (width / 3) * 2,
                         height * 0.6 if player_number > 1 else height * 0.8,
                         width / 3,
                         height * 0.2),
                        Color.white, Color.black, self.big_font)
