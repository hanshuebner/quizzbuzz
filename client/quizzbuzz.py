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
from buzzers import Buzzers
from questions import QuestionsServer
os.putenv('SDL_VIDEODRIVER', 'fbcon')

def main(buzzer_device):
    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()

    buzzer_sounds = [pygame.mixer.Sound('../resources/sounds/buzzer-0.wav'),
                     pygame.mixer.Sound('../resources/sounds/buzzer-1.wav'),
                     pygame.mixer.Sound('../resources/sounds/buzzer-2.wav'),
                     pygame.mixer.Sound('../resources/sounds/buzzer-3.wav')]

    clock = pygame.time.Clock()
    buzzers = Buzzers(buzzer_device)
    display = Display()
    question = None
    scores = [0, 0, 0, 0]

    def play_round(questions):
        view = views.QuestionView(display)
        while len(questions) > 0:
            question = questions.pop()
            view.display_choices(question.question, question.answers)

            answered = [False, False, False, False]
            buzzers.leds(*answered)
            correct_answer = False
            while not(correct_answer):
                pressed = buzzers.get_pressed()
                if pressed:
                    player_index = pressed['buzzer']
                    button = pressed['button']
                    if button == 0:
                        buzzer_sounds[player_index].play()
                    else:
                        if not(answered[player_index]):
                            answered[player_index] = True
                            buzzers.leds(*answered)
                            if question.answers[4 - button] == question.correct_answer:
                                buzzer_sounds[player_index].play()
                                scores[player_index] = scores[player_index] + 1
                                view.set_score(player_index, scores[player_index])
                                view.display_choices(question.question, question.answers, correct=question.correct_answer)
                                view.set_player_answered(player_index, True)
                                correct_answer = True
                            else:
                                view.set_player_answered(player_index, False)

                clock.tick(10)
                pygame.display.flip()

            pygame.time.delay(1000)
            while buzzers.get_pressed() != None:
                None

    server = QuestionsServer()

    category = server.categories()[0]

    questions = server.questions(category=category)
    play_round(questions)


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
