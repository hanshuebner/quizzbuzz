import pygame

class Player:
    def __init__(self, name, level, index):
        self.name = name
        self.level = level
        self.index = index
        self.score = 0
        self.sound = pygame.mixer.Sound('../resources/sounds/buzzer-' + str(index) + '.wav')
        self.buzzer = None

    def add_score(self, points):
        self.score += points
