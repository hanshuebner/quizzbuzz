#!/usr/bin/python3

import sys
import pygame
import os
import time
import random
import json
import threading
import display
from display import Display
import views
import models
from buzzers import BuzzerController, Red, Blue, Orange, Green, Yellow
from questions import QuestionsServer

os.putenv('SDL_VIDEODRIVER', 'fbcon')

def load_player_names():
    with open('../database/players.json', 'r') as file:
        return json.load(file)

def choose_players(display, buzzers):
    clock = pygame.time.Clock()
    all_player_names = load_player_names()
    view = views.ChoosePlayerView(display, load_player_names())
    pygame.display.flip()
    unassigned_buzzers = set(buzzers.buzzers)
    claimed_buzzers = {}
    while True:
        message = buzzers.get_pressed()
        if message:
            buzzer = message.buzzer
            if buzzer in unassigned_buzzers:
                unassigned_buzzers.remove(buzzer)
                claimed_buzzers[buzzer] = 0
                buzzer.set_led(True)
            elif buzzer in claimed_buzzers:
                if message.button == Blue and claimed_buzzers[buzzer] > 0:
                    claimed_buzzers[buzzer] = claimed_buzzers[buzzer] - 1
                elif message.button == Orange and claimed_buzzers[buzzer] < len(all_player_names) - 1:
                    claimed_buzzers[buzzer] = claimed_buzzers[buzzer] + 1
                elif message.button == Red and len(set(claimed_buzzers.values())) == len(claimed_buzzers):
                    break
        for buzzer in claimed_buzzers:
            view.display_name_column(buzzer.index, all_player_names[claimed_buzzers[buzzer]])
        pygame.display.flip()
        clock.tick(10)

    def make_player(entry):
        index, buzzer = entry
        player = models.Player(all_player_names[claimed_buzzers[buzzer]], index)
        buzzer.set_player(player)
        buzzer.set_led(False)
        return player

    return list(map(make_player, enumerate(claimed_buzzers)))

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
                    if button == Red:
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
            if message and message.button == Red:
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
    players = choose_players(display, buzzers)

    # select category
    category = choose_category(display, buzzers, random.sample(server.categories(), 4), who_chooses(players))
    questions = server.questions(category=category)

    # play
    play_round(display, buzzers, players, questions)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
