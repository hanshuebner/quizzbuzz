#!/usr/bin/python3

import sys
import pygame
import os
import time
import random
import json
import threading
import display
import game_modes
from enum import Enum
from display import Display
import views
import models
from buzzers import BuzzerController, Red, Blue, Orange, Green, Yellow
from questions import QuestionsServer

os.putenv('SDL_VIDEODRIVER', 'fbcon')

def now():
    return pygame.time.get_ticks()

def delay(buzzers, milliseconds):
    pygame.time.delay(3000)
    buzzers.flush()

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
        clock.tick(10)

    def make_player(entry):
        index, buzzer = entry
        player = models.Player(all_player_names[claimed_buzzers[buzzer]], index)
        buzzer.set_player(player)
        buzzer.set_led(False)
        return player

    return list(map(make_player, enumerate(claimed_buzzers)))

def simple_view(view, buzzers):
    clock = pygame.time.Clock()
    start = now()
    while True:
        message = buzzers.get_pressed()
        if message and message.button == 0:
            break
        clock.tick(10)
        elapsed = now() - start
        if elapsed >= 600:
            buzzers.set_all_leds(False)
            start = now()
        elif elapsed >= 300:
            buzzers.set_all_leds(True)
    buzzers.set_all_leds(False)

def describe_game_mode(display, buzzers, mode):
    title, text = mode.description()
    view = views.DescribeGameModeView(display, title, text)
    simple_view(view, buzzers)

def choose_category(display, buzzers, categories, player):
    clock = pygame.time.Clock()
    player.buzzer.set_led(True)
    view = views.ChooseCategoryView(display, player.name, categories)
    category = None
    while not(category):
        message = buzzers.get_pressed()
        if message and message.buzzer.player == player and message.button != 0:
            category = categories[4 - message.button]
        clock.tick(10)
    view.display_categories(category)
    delay(buzzers, 3000)
    player.buzzer.set_led(False)
    return category

def play_round(display, buzzers, players, questions, round_mode):
    clock = pygame.time.Clock()
    while len(questions) > 0:
        question = questions.pop()

        view = views.QuestionView(display, players, question.question)

        delay(buzzers, 3000)

        view.display_choices(question.answers)

        answered = set()

        answer_is_correct = False
        remaining_time = 10000

        while not(round_mode.question_complete(players, answered, answer_is_correct, remaining_time)):
            base_time = now()
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
                            answer_is_correct = question.answers[4 - button] == question.correct_answer
                            player.sound.play()
                            player.add_score(round_mode.score(answer_is_correct, remaining_time))
                            view.draw_player(player, answer_is_correct)

            clock.tick(10)
            remaining_time -= now() - base_time

        view.display_choices(question.answers, correct=question.correct_answer)

        delay(buzzers, 3000)

        buzzers.set_all_leds(False)

def victory_ceremony(display, buzzers, players):
    ranked = sorted(players, key=lambda player: -player.score)
    view = views.VictoryCeremonyView(display, list(map(lambda player: (player.name, player.score), ranked)))
    simple_view(view, buzzers)

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

    questions_per_round = 7

    while True:
        players = choose_players(display, buzzers)

        for mode in [game_modes.Relaxed(), game_modes.Timed(), game_modes.OneOnly(), game_modes.Final()]:
            describe_game_mode(display, buzzers, mode)

            category = choose_category(display, buzzers, random.sample(server.categories(), 4), who_chooses(players))
            questions = server.questions(category=category, question_count=questions_per_round)

            play_round(display, buzzers, players, questions, mode)

        victory_ceremony(display, buzzers, players)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
