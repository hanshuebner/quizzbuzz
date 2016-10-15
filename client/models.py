import pygame

class Player:
    def __init__(self, name, index):
        self.name = name
        self.score = 0
        self.index = index
        self.sound = pygame.mixer.Sound('../resources/sounds/buzzer-' + str(index) + '.wav')

    def add_score(self, points):
        self.score = self.score + 1
