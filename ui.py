import pygame
from pygame.locals import *
from constants import *

class UI:
    def __init__(self):
        self.start_but = Rect(100, 25, UNIT_WIDTH, UNIT_HEIGHT)
        self.start_but_pressed = Rect(105, 30, UNIT_WIDTH - 10, UNIT_HEIGHT - 10)
        self.end_but = Rect(150, 25, UNIT_WIDTH, UNIT_HEIGHT)
        self.end_but_pressed = Rect(155, 30, UNIT_WIDTH - 10, UNIT_HEIGHT - 10)
        self.clear_but = Rect(700, 25, UNIT_WIDTH, UNIT_HEIGHT)
        self.run_but = Rect(750, 25, UNIT_WIDTH, UNIT_HEIGHT)
        self.window = Rect(0, 0, SIZE[0], SIZE[1] - 1000)
        self.end_pressed = False
        self.start_pressed = True

    def draw(self, screen):
        pygame.draw.rect(screen, LGRAY, self.window)
        pygame.draw.rect(screen, PURPLE, self.start_but)
        pygame.draw.rect(screen, GREEN, self.end_but)
        pygame.draw.rect(screen, WHITE, self.clear_but)
        pygame.draw.rect(screen, WHITE, self.run_but)

        if self.start_pressed:
            pygame.draw.rect(screen, DPURPLE, self.start_but_pressed)

        if self.end_pressed:
            pygame.draw.rect(screen, DGREEN, self.end_but_pressed)

    def update(self):
        pygame.display.update(self.window)
        pygame.display.update(self.start_but)
        pygame.display.update(self.end_but)

    def press_start(self):
        self.start_pressed = True

    def unpress_start(self):
        self.start_pressed = False

    def press_end(self):
        self.end_pressed = True

    def unpress_end(self):
        self.end_pressed = False
