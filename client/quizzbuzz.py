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

def main():
    buzz_sound_file = '../resources/sounds/buzzer.wav'

    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()

    clock = pygame.time.Clock()
    buzzers = Buzzers('/dev/hidraw0')
    display = Display()
    question = None

    def next_question():
        question = Question('http://localhost:3399')
        display.set_question(question.question, question.answers)

    next_question()

    while True:
        pressed = buzzers.get_pressed()
        if pressed:
            if not(pygame.mixer.music.get_busy()):
                pygame.mixer.music.load(buzz_sound_file)
                pygame.mixer.music.play()
            print(pressed)
            next_question()

        subseconds = math.modf(time.time())[0]
        led_state = (subseconds > 0.9) or (subseconds > 0.7 and subseconds < 0.8)
        buzzers.leds(led_state, led_state, led_state, led_state)

        clock.tick(10)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('exiting')
        exit(0)
    except:
        raise
