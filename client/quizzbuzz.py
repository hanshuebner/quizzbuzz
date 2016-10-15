#!/usr/bin/python3

import sys
import pygame
import os
import time
import math
import threading
import display
from display import Display
import views
import models
from buzzers import Buzzers
from questions import QuestionsServer

os.putenv('SDL_VIDEODRIVER', 'fbcon')

def play_round(display, buzzers, players, questions):
    question = None
    clock = pygame.time.Clock()
    view = views.QuestionView(display, players)
    while len(questions) > 0:
        question = questions.pop()
        view.display_choices(question.question, question.answers)

        answered = {}

        def set_buzzer_leds():
            #buzzers.leds(*answered)
            None

        set_buzzer_leds()

        correct_answer = False
        while not(correct_answer):
            pressed = buzzers.get_pressed()
            if pressed:
                player = pressed['player']
                button = pressed['button']
                if player:
                    if button == 0:
                        player.sound.play()
                    else:
                        if not(answered.get(player, False)):
                            answered[player] = True
                            set_buzzer_leds()
                            if question.answers[4 - button] == question.correct_answer:
                                player.sound.play()
                                player.add_score(1)
                                view.set_score(player.index, player.score)
                                view.display_choices(question.question, question.answers, correct=question.correct_answer)
                                view.set_player_answered(player.index, True)
                                correct_answer = True
                            else:
                                view.set_player_answered(player.index, False)

            clock.tick(10)
            pygame.display.flip()

        pygame.time.delay(1000)
        while buzzers.get_pressed() != None:
            None

def main(buzzer_device):
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()

    buzzers = Buzzers(buzzer_device)
    display = Display()
    server = QuestionsServer()

    category = server.categories()[0]
    questions = server.questions(category=category)
    players = [models.Player('Alva', 0), models.Player('Marna', 1), models.Player('Hans', 2)]
    buzzers.set_player(0, players[0])
    buzzers.set_player(1, players[1])
    buzzers.set_player(2, players[2])
    play_round(display, buzzers, players, questions)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
