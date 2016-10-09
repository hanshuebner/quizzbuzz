#!/usr/bin/python3

import pygame
import os
import time
import math
import threading
from textrect import render_textrect
from buzzers import Buzzers
os.putenv('SDL_VIDEODRIVER', 'fbcon')

def main():
    buzz_sound_file = '../resources/sounds/buzzer.wav'

    pygame.mixer.init(44100, -16, 2, 512)
    pygame.init()
    pygame.display.init()
    pygame.mouse.set_visible(0)

    font = pygame.font.Font("../resources/fonts/BalooThambi-Regular.ttf", 96)
    info = pygame.display.Info()
    display = pygame.display.set_mode((info.current_w, info.current_h))

    pygame.mixer.music.load(buzz_sound_file)
    
    pygame.mixer.music.play()
    pygame.mixer.music.pause()

    clock = pygame.time.Clock()
    buzzers = Buzzers('/dev/hidraw0')

    label = render_textrect('Wie heißt das Reh mit Vornamen?',
                            font, pygame.Rect(0, 0, 1920, 400),
                            (195, 252, 174), (0, 0, 0),
                            justification=1)
    buzz_label = font.render('Buzz!', 1, (195, 180, 174))

    while True:
        display.blit(label, (0, 0))

        pressed = buzzers.get_pressed()
        if pressed:
            print(pressed)

        subseconds = math.modf(time.time())[0]
        led_state = (subseconds > 0.9) or (subseconds > 0.7 and subseconds < 0.8)
        buzzers.leds(led_state, led_state, led_state, led_state)

        if led_state:
            display.blit(buzz_label, (0, 800))
        else:
            display.fill(pygame.Color('black'), (0, 800, 400, 200))

        # pygame.mixer.music.play()

        # while pygame.mixer.music.get_busy():
        #  pygame.time.Clock().tick(10)

        clock.tick(10)
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit(0)
