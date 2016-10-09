#!/usr/bin/python3

import sys
import pygame
import os
import time
import math
import threading
from display import Display
from buzzers import Buzzers
from questions import Question
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

    def next_question():
        question = Question('http://localhost:3399')
        display.set_question(question.question, question.answers)
        return question

    while True:
        question = next_question()

        buzzers.leds(True, True, True, True)
        correct_answer = False
        while not(correct_answer):
            pressed = buzzers.get_pressed()
            if pressed:
                player_index = pressed['buzzer']
                button = pressed['button']
                if button == 0:
                    buzzer_sounds[player_index].play()
                else:
                    if question.answers[4 - button] == question.correct_answer:
                        buzzer_sounds[player_index].play()
                        scores[player_index] = scores[player_index] + 1
                        display.set_score(player_index, scores[player_index])
                        display.set_question(question.question, question.answers, correct=question.correct_answer)
                        correct_answer = True

            clock.tick(10)
            pygame.display.flip()

        pygame.time.delay(1000)
        while buzzers.get_pressed() != None:
            None

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
