import pygame
from .settings import *


class Lifebar:
    def __init__(self, x, y, width, height, max_health, color1=GREEN, color2=RED):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dimension = (self.width, self.height)
        self.color1 = color1
        self.color2 = color2

        self.max_health = max_health
        self.health = max_health

        self.rrect = pygame.Rect(x, y, width, height)
        self.grect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        self.update()
        pygame.draw.rect(screen, self.color2, self.rrect)
        pygame.draw.rect(screen, self.color1, self.grect)

    def update(self):
        green_width = self.health / self.max_health * self.width
        self.grect = self.grect = pygame.Rect(self.x, self.y, green_width, self.height)

    def take_damage(self, damage):
        self.health -= damage 
        if self.health <= 0:
            self.health = 0

    def set_center_position(self, center):
        self.x = center[0] - self.width / 2
        self.y = center[1] - self.height / 2
        self.rrect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.grect = pygame.Rect(self.x, self.y, self.width, self.height)
