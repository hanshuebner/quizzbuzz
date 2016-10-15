#!/usr/bin/python3

import pygame
from display import Display, Color

class Screen:
    def __init__(self, display):
        self.display = display
        display.clear()

class ChoosePlayerScreen(Screen):
    def __init__(self, display, player_names):
        super().__init__(display)
        self.player_names = player_names
        self.display.draw_label('Wer spielt mit?', (0, 0, self.display.width, self.display.height), font='big')

    def display_name_column(self, buzzer_index, chosen, unavailable):
        cell_width = self.display.width / 4
        for name_index, name in enumerate(self.player_names):
            foreground = Color.black if name == chosen else Color.grey if name in unavailable else Color.white
            background = Color.white if name == chosen else Color.black
            self.display.draw_label(name,
                                    (buzzer_index * cell_width, 200 + name_index * 70, cell_width, 70),
                                    foreground, background)
        def make_label(index, string, color, font='normal'):
            self.display.draw_label(string, (cell_width * index, self.display.height - 70, cell_width, 70), Color.black, color, font)
        make_label(0, '\ue030', Color.blue, 'icons')
        make_label(1, '\ue02d', Color.orange, 'icons')
        make_label(3, 'Fertig', Color.red)

class QuestionScreen(Screen):
    def __init__(self, display, players):
        super().__init__(display)
        self.players = players
        for i in range(len(players)):
            (x, y, width, height) = self.player_rect(i)
            self.display.draw_label(players[i]['name'], (x, y + 120, width, height - 120))
            self.set_score(i, players[i]['score'])

    def player_rect(self, index):
        width = self.display.width
        height = self.display.height
        return (0 if (index % 2) == 0 else (width / 3) * 2,
                height * 0.6 if index < 2 else height * 0.8,
                width / 3,
                height * 0.2)

    def set_score(self, player_number, score):
        (x, y, width, height) = self.player_rect(player_number)
        self.display.draw_label(str(score), (x, y, width, height - 100), font='big')

    def draw_answer(self, text, correct, rect, color):
        inverse = correct == None or text == correct
        self.display.draw_label(text,
                                rect,
                                Color.black if inverse else color,
                                color if inverse else Color.black)

    def display_choices(self, question, answers, correct=None):
        width = self.display.width
        height = self.display.height
        self.display.draw_label(question, (0, 0, width, height * 0.6), font='big')
        self.draw_answer(answers[0], correct, (width / 3, height * 0.6, width / 3, 70), Color.blue)
        self.draw_answer(answers[1], correct, (width / 3, height * 0.7, width / 3, 70), Color.orange)
        self.draw_answer(answers[2], correct, (width / 3, height * 0.8, width / 3, 70), Color.green)
        self.draw_answer(answers[3], correct, (width / 3, height * 0.9, width / 3, 70), Color.yellow)
        for player in range(len(self.players)):
            self.set_player_answered_color(player, Color.black)

    def set_player_answered_color(self, player_number, color):
        width = self.display.width
        height = self.display.height
        x = int(80 if (player_number % 2) == 0 else width - 80)
        y = int(height * 0.67 if player_number < 2 else height * 0.87)
        self.display.draw_circle(color, (x, y), 48)

    def set_player_answered(self, player_number, correct):
        self.set_player_answered_color(player_number, (Color.green if correct else Color.red))

def test_question(display):
    screen = QuestionScreen(display, [{'name': 'Alva', 'score': 23},
                                      {'name': 'Marna', 'score': 20},
                                      {'name': 'Hans', 'score': 12}])
    screen.display_choices('Wie heisst der Bürgermeister von Wesel?',
                           ['Esel', 'Esel', 'Esel', 'Esel'])

def test_choose_player(display):
    screen = ChoosePlayerScreen(display, ['Alva', 'Marna', 'Hans', 'Gertraude', 'Michaela'])
    unavailable = set(['Alva', 'Marna', 'Hans'])
    screen.display_name_column(0, 'Alva', unavailable)
    screen.display_name_column(1, 'Marna', unavailable)
    screen.display_name_column(3, 'Hans', unavailable)

if __name__ == '__main__':
    try:
        pygame.init()
        display = Display()
        test_choose_player(display)
        pygame.display.flip()
        input()
        test_question(display)
        pygame.display.flip()
        input()
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
