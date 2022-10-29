import pygame
from .settings import *


class Camera:
    def __init__(self, screen):
        self.screen = screen
        self.offset = pygame.math.Vector2(100, 100)

    def set_center_target(self, target):
        self.target = target

    def center_target_position(self):
        self.offset.x = self.target.rect.centerx - WINDOW_SIZE[0] // 2
        self.offset.y = self.target.rect.centery - WINDOW_SIZE[1] // 2

    def update(self, entity):
        self.center_target_position()
        entity.rect.topleft-= self.offset
        entity.x -= self.offset.x
        entity.y -= self.offset.y

    def update_all(self, entities):
        self.center_target_position()
        for entity in entities.values():
            entity.rect.topleft -= self.offset
            entity.rect.x -= self.offset.x
            entity.rect.y -= self.offset.y
            
    def get_world_pos(self, rect):
        return rect.x - self.offset.x, rect.y - self.offset.y
