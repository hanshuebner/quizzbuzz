
import pygame
from textrect import render_textrect
from enum import Enum

class Color(Enum):
    blue = pygame.Color('#0076CE')
    orange = pygame.Color('#E85719')
    red = pygame.Color('#AF0505')
    white = pygame.Color('#FFFFFF')
    grey = pygame.Color('#7F7F7F')
    yellow = pygame.Color('#F2C605')
    green = pygame.Color('#4BAE03')
    black = pygame.Color('#000000')

font_dir = "../resources/fonts/"
text_font = "Exo-SemiBold.ttf"
icon_font = "open-iconic.ttf"

def load_font(name, size):
    return pygame.font.Font(font_dir + name, size)

class Display:
    def __init__(self):
        pygame.display.init()
        pygame.mouse.set_visible(0)
        self.info = pygame.display.Info()
        self.display = pygame.display.set_mode((self.info.current_w, self.info.current_h))
        self.width = self.info.current_w
        self.height = self.info.current_h
        self.fonts = {'normal': load_font(text_font, 48),
                      'big': load_font(text_font, 70),
                      'huge': load_font(text_font, 192),
                      'icons': load_font(icon_font, 48)}

    def clear(self):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, self.width, self.height))

    def draw_label(self, text, rect, foreground=Color.white, background=Color.black, font='normal'):
        self.display.blit(render_textrect(text,
                                          self.fonts[font],
                                          pygame.Rect(0, 0, rect[2], rect[3]),
                                          foreground.value,
                                          background.value,
                                          justification=1),
                          (rect[0], rect[1]))

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.display, color.value, center, 48)

