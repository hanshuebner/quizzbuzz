#!/usr/bin/python3

import sys
import pygame
import os
import time
import random
import threading
import display
from display import Display
import views
import models
from buzzers import BuzzerController
from questions import QuestionsServer

os.putenv('SDL_VIDEODRIVER', 'fbcon')

def choose_category(display, buzzers, categories, player):
    clock = pygame.time.Clock()
    player.buzzer.set_led(True)
    view = views.ChooseCategoryView(display, player.name, categories)
    pygame.display.flip()
    category = None
    while not(category):
        message = buzzers.get_pressed()
        if message and message.buzzer.player == player and message.button != 0:
            category = categories[4 - message.button]
        clock.tick(10)
    view.display_categories(category)
    pygame.display.flip()
    pygame.time.delay(3000)
    player.buzzer.set_led(False)
    return category

def play_round(display, buzzers, players, questions):
    clock = pygame.time.Clock()
    view = views.QuestionView(display, players)
    while len(questions) > 0:
        question = questions.pop()
        view.display_choices(question.question, question.answers)

        answered = set()

        correct_answer = False
        while not(correct_answer) and len(answered) < len(players):
            message = buzzers.get_pressed()
            if message:
                player = message.buzzer.player
                button = message.button
                if player:
                    if button == 0:
                        player.sound.play()
                    else:
                        if not(player in answered):
                            answered.add(player)
                            player.buzzer.set_led(True)
                            if question.answers[4 - button] == question.correct_answer:
                                player.sound.play()
                                player.add_score(1)
                                view.set_score(player.index, player.score)
                                view.set_player_answered(player.index, True)
                                correct_answer = True
                            else:
                                view.set_player_answered(player.index, False)

            clock.tick(10)
            pygame.display.flip()

        view.display_choices(question.question, question.answers, correct=question.correct_answer)
        pygame.display.flip()

        pygame.time.delay(1000)
        buzzers.flush()

        def set_all_leds(state):
            for player in players:
                player.buzzer.set_led(state)

        set_all_leds(True)

        while True:
            message = buzzers.get_pressed()
            if message and message.button == 0:
                break
            clock.tick(10)

        set_all_leds(False)

def who_chooses(players):
    ranked = sorted(players, key=lambda player: player.score)
    low = ranked[0].score
    losers = list(filter(lambda player: player.score == low, ranked))
    return random.choice(losers)

def main(buzzer_device):
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()

    buzzers = BuzzerController(buzzer_device)
    display = Display()
    server = QuestionsServer()

    # select players
    players = [models.Player('Alva', 0), models.Player('Marna', 1), models.Player('Hans', 2)]
    for i in range(3):
        buzzers.buzzers[i].set_player(players[i])

    # select category
    category = choose_category(display, buzzers, random.sample(server.categories(), 4), who_chooses(players))
    print(category)
    #questions = server.questions(category=category)

    # play
    #play_round(display, buzzers, players, questions)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
