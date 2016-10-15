
import pygame
from textrect import render_textrect

class Display:
    def __init__(self):
        pygame.display.init()
        pygame.mouse.set_visible(0)
        self.font_path = "../resources/fonts/Exo-SemiBold.ttf"
        self.big_font = pygame.font.Font(self.font_path, 96)
        self.font = pygame.font.Font(self.font_path, 48)
        self.info = pygame.display.Info()
        self.display = pygame.display.set_mode((self.info.current_w, self.info.current_h))
        self.width = self.info.current_w
        self.height = self.info.current_h

    def draw_label(self, text, rect, foreground, background, font):
        self.display.blit(render_textrect(text,
                                          font,
                                          pygame.Rect(0, 0, rect[2], rect[3]),
                                          foreground.value,
                                          background.value,
                                          justification=1),
                          (rect[0], rect[1]))

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.display, color.value, center, 48)

