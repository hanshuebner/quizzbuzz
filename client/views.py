#!/usr/bin/python3

import pygame
from display import Display, Color

class View:
    def __init__(self, display):
        self.display = display
        display.clear()

class ChoosePlayerView(View):
    def __init__(self, display, player_names, ip_address='127.0.0.1'):
        super().__init__(display)
        self.player_names = player_names
        self.display.draw_label('Wer spielt mit?', (0, 0, self.display.width, self.display.height), font='big')
        self.display.draw_label(ip_address, (0, 0, 200, 100), font='small')

    def display_name_column(self, buzzer_index, chosen, unavailable=set()):
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
        pygame.display.flip()

class DescribeGameModeView(View):
    def __init__(self, display, title, description):
        super().__init__(display)
        self.display.draw_label(title,
                                (0, 0, self.display.width, self.display.height / 3),
                                font='huge')
        self.display.draw_label(description,
                                (0, self.display.height / 3, self.display.width, 2 * (self.display.height / 3)),
                                font='big')
        pygame.display.flip()

class ChooseCategoryView(View):
    def __init__(self, display, player_name, categories):
        super().__init__(display)
        self.display.draw_label(player_name + ', wähle die Kategorie!',
                                (0, 0, self.display.width, self.display.height),
                                font='big')
        self.categories = categories
        self.display_categories()

    def draw_category(self, text, chosen, rect, color):
        inverse = chosen == None or text == chosen
        self.display.draw_label(text,
                                rect,
                                Color.black if inverse else color,
                                color if inverse else Color.black,
                                font='big')

    def display_categories(self, chosen=None):
        width = self.display.width
        height = self.display.height
        self.draw_category(self.categories[0], chosen, (width * 0.18, height * 0.4 + 0, width * 0.64, 100), Color.blue)
        self.draw_category(self.categories[1], chosen, (width * 0.18, height * 0.4 + 110, width * 0.64, 100), Color.orange)
        self.draw_category(self.categories[2], chosen, (width * 0.18, height * 0.4 + 2*110, width * 0.64, 100), Color.green)
        self.draw_category(self.categories[3], chosen, (width * 0.18, height * 0.4 + 3*110, width * 0.64, 100), Color.yellow)
        pygame.display.flip()

class QuestionView(View):
    def __init__(self, display, players, question):
        super().__init__(display)
        self.players = players
        width = self.display.width
        height = self.display.height
        self.display.draw_label(question, (0, 0, width, height * 0.4), font='big')
        for player in players:
            self.draw_player(player)
        pygame.display.flip()

    def player_rect(self, index):
        width = self.display.width
        height = self.display.height
        return (0 if (index % 2) == 0 else width - (width * 0.17),
                (height * 0.41) if index < 2 else (height * 0.65),
                width * 0.17,
                height * 0.2)

    def draw_answer(self, text, correct, rect, color):
        inverse = correct == None or text == correct
        self.display.draw_label(text,
                                rect,
                                Color.black if inverse else color,
                                color if inverse else Color.black,
                                font='big')

    def display_question(self, question):
        pygame.display.flip()

    def display_choices(self, answers, correct=None):
        width = self.display.width
        height = self.display.height
        self.draw_answer(answers[0], correct, (width * 0.18, height * 0.4 + 0, width * 0.64, 100), Color.blue)
        self.draw_answer(answers[1], correct, (width * 0.18, height * 0.4 + 110, width * 0.64, 100), Color.orange)
        self.draw_answer(answers[2], correct, (width * 0.18, height * 0.4 + 2*110, width * 0.64, 100), Color.green)
        self.draw_answer(answers[3], correct, (width * 0.18, height * 0.4 + 3*110, width * 0.64, 100), Color.yellow)
        pygame.display.flip()

    def draw_player(self, player, answer_is_correct=None):
        (x, y, width, height) = self.player_rect(player.index)
        foreground, background = Color.white, Color.black
        if answer_is_correct == True:
            foreground, background = Color.black, Color.green
        elif answer_is_correct == False:
            foreground, background = Color.black, Color.red
        self.display.draw_label(player.name, (x, y + 90, width, 66), foreground=foreground, background=background)
        self.display.draw_label(str(player.score), (x, y, width, height - 66), font='big')
        pygame.display.flip()

class VictoryCeremonyView(View):
    def __init__(self, display, scoreboard):
        super().__init__(display)
        width = self.display.width
        height = self.display.height
        self.display.draw_label('Siegerehrung',
                                (0, 0, width, 250),
                                font='huge')
        self.display.draw_label('Rang', (0, 250, width * 0.2, 100), font='big', foreground=Color.grey)
        self.display.draw_label('Name', (width * 0.2, 250, width * 0.6, 100), font='big', foreground=Color.grey)
        self.display.draw_label('Punkte', (width * 0.8, 250, width * 0.2, 100), font='big', foreground=Color.grey)
        for rank, player in enumerate(scoreboard):
            name, score = player
            self.display.draw_label(str(rank + 1), (0, 350 + rank * 100, width * 0.2, 100), font='big')
            self.display.draw_label(name, (width * 0.2, 350 + rank * 100, width * 0.6, 100), font='big')
            self.display.draw_label(str(score), (width * 0.8, 350 + rank * 100, width * 0.2, 100), font='big')
        pygame.display.flip()

def test_choose_player(display):
    view = ChoosePlayerView(display, ['Alva', 'Marna', 'Hans', 'Gertraude', 'Michaela'])
    unavailable = set(['Alva', 'Marna', 'Hans'])
    view.display_name_column(0, 'Alva', unavailable)
    view.display_name_column(1, 'Marna', unavailable)
    view.display_name_column(3, 'Hans', unavailable)

def test_choose_category(display):
    view = ChooseCategoryView(display,
                                  'Alva',
                                  ['Filme', 'Wirtschaft', 'Musik', 'Religion & Gesellschaft'])

def test_question(display):
    players = [models.Player('Alva', 0),
               models.Player('Marna', 1),
               models.Player('Hans', 2)]
    for player in players:
        player.score = 9999
    view = QuestionView(display,
                        players,
                        'Wie heisst der Bürgermeister von Wesel?')
    input()
    view.display_choices(["Das Quiz mit Jörg Pilawa",
                          "Yellowstone-Nationalpark",
                          "Gustave Alexandre Eiffel",
                          "1.000.000 Million Dollar"])
    view.draw_player(players[0], True)
    view.draw_player(players[1], True)
    view.draw_player(players[2], False)
    input()
    view.display_choices(["Das Quiz mit Jörg Pilawa",
                          "Yellowstone-Nationalpark",
                          "Gustave Alexandre Eiffel",
                          "1.000.000 Million Dollar"],
                         "1.000.000 Million Dollar")

def test_siegerehrung(display):
    view = VictoryCeremonyView(display, (('Marna', 3848), ('Alva', 3302), ('Hans', 2003)))

if __name__ == '__main__':
    import models
    try:
        pygame.init()
        display = Display()
        test_choose_player(display)
        input()
        test_choose_category(display)
        input()
        test_question(display)
        input()
        test_siegerehrung(display)
        input()
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
