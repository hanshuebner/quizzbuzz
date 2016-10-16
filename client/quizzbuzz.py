#!/usr/bin/python3

import sys
import pygame
import os
import time
import random
import json
import threading
import display
from enum import Enum
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
                    claimed_buzzers[buzzer] -= 1
                elif message.button == Orange and claimed_buzzers[buzzer] < len(all_player_names) - 1:
                    claimed_buzzers[buzzer] += 1
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

class RoundMode(Enum):
    relaxed = 0
    timed = 1
    one_only = 2
    final = 3

def play_round(display, buzzers, players, questions, round_mode):
    clock = pygame.time.Clock()
    view = views.QuestionView(display, players)
    while len(questions) > 0:
        question = questions.pop()
        view.display_choices(question.question, question.answers)

        answered = set()

        answer_correct = False
        remaining_time = 10000

        # When does is the question complete?
        def all_answered():
            return len(answered) == len(players)

        def time_remaining():
            return remaining_time == 0 or len(answered) == len(players)

        def one_correct_answer():
            return answer_correct or len(answered) == len(players)

        # How is the score calculated
        def simple_score(answer_is_correct):
            if answer_is_correct:
                return 250
            else:
                return 0

        def time_score(answer_is_correct):
            if answer_is_correct:
                return int(remaining_time / 40)
            else:
                return 0

        def win_and_loose(answer_is_correct):
            if answer_is_correct:
                return 250
            else:
                return -250

        if round_mode == RoundMode.relaxed:
            question_complete = all_answered
            scoring = simple_score
        elif round_mode == RoundMode.timed:
            question_complete = time_remaining
            scoring = time_score
        elif round_mode == RoundMode.one_only:
            question_complete = one_correct_answer
            scoring = simple_score
        elif round_mode == RoundMode.final:
            question_complete = one_correct_answer
            scoring = win_and_loose
        else:
            raise Exception('Unknown round mode')

        while not(question_complete()):
            base_time = pygame.time.get_ticks()
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
                            answer_correct = question.answers[4 - button] == question.correct_answer
                            player.sound.play()
                            player.add_score(scoring(answer_correct))
                            view.set_score(player.index, player.score)
                            view.set_player_answered(player.index, answer_correct)

            pygame.display.flip()
            clock.tick(10)
            remaining_time -= pygame.time.get_ticks() - base_time

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

    for mode in [RoundMode.relaxed, RoundMode.timed, RoundMode.one_only, RoundMode.final]:
        # select category
        category = choose_category(display, buzzers, random.sample(server.categories(), 4), who_chooses(players))
        questions = server.questions(category=category, question_count=3)

        # play
        play_round(display, buzzers, players, questions, mode)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
