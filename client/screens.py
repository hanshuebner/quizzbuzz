#!/usr/bin/python3

import pygame
from display import Display
from enum import Enum

class Color(Enum):
    blue = pygame.Color('#0076CE')
    orange = pygame.Color('#E85719')
    red = pygame.Color('#AF0505')
    white = pygame.Color('#FFFFFF')
    yellow = pygame.Color('#F2C605')
    green = pygame.Color('#4BAE03')
    black = pygame.Color('#000000')

class Screen:
    def __init__(self, display):
        self.display = display

class QuestionScreen(Screen):
    def __init__(self, display, players):
        super().__init__(display)
        for i in range(len(players)):
            self.set_score(i, 0)

    def draw_answer(self, text, correct, rect, color):
        inverse = correct == None or text == correct
        self.display.draw_label(text,
                                rect,
                                Color.black if inverse else color,
                                color if inverse else Color.black,
                                self.display.font)

    def display_choices(self, question, answers, correct=None):
        width = self.display.width
        height = self.display.height
        self.display.draw_label(question, (0, 0, width, height * 0.6), Color.white, Color.black, self.display.big_font)
        self.draw_answer(answers[0], correct, (width / 3, height * 0.6, width / 3, 70), Color.blue)
        self.draw_answer(answers[1], correct, (width / 3, height * 0.7, width / 3, 70), Color.orange)
        self.draw_answer(answers[2], correct, (width / 3, height * 0.8, width / 3, 70), Color.green)
        self.draw_answer(answers[3], correct, (width / 3, height * 0.9, width / 3, 70), Color.yellow)
        for player in range(4):
            self.set_player_answered_color(player, Color.black)

    def set_player_answered_color(self, player_number, color):
        width = self.display.width
        height = self.display.height
        x = int(80 if (player_number % 2) == 0 else width - 80)
        y = int(height * 0.67 if player_number > 1 else height * 0.87)
        self.display.draw_circle(color, (x, y), 48)

    def set_player_answered(self, player_number, correct):
        self.set_player_answered_color(player_number, (Color.green if correct else Color.red))

    def set_score(self, player_number, score):
        width = self.display.width
        height = self.display.height
        self.display.draw_label(str(score),
                                (0 if (player_number % 2) == 0 else (width / 3) * 2,
                                 height * 0.6 if player_number > 1 else height * 0.8,
                                 width / 3,
                                 height * 0.2),
                                Color.white, Color.black, self.display.big_font)

if __name__ == '__main__':
    try:
        pygame.init()
        display = Display()
        screen = QuestionScreen(display, ['Alva', 'Marna', 'Hans')
        screen.display_choices('Wie heisst der Bürgermeister von Wesel?',
                               ['Esel', 'Esel', 'Esel', 'Esel'])
        pygame.display.flip()
        input()
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
