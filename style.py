import pygame
from constants import *

class Style:
    def __init__(self, screen):
        self.screen = screen
        self.clear_img = pygame.image.load('img/clear.png')
        self.play_img = pygame.image.load('img/play.png')

    def draw(self):
        self.screen.blit(self.clear_img, (700, 25))
        self.screen.blit(self.play_img, (750, 25))

        # borders
        pygame.draw.line(self.screen, GRAY, (0, 100), (1000, 100), 7)
        pygame.draw.line(self.screen, GRAY, (0, 1100), (1000, 1100), 7)
        pygame.draw.line(self.screen, GRAY, (0, 100), (0, 1100), 7)
        pygame.draw.line(self.screen, GRAY, (1000, 100), (1000, 1100), 7)
