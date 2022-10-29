from math import ceil
from .common.settings import *
from .common.ui_utils import *


class Player:
    def __init__(self, total_columns, x=WINDOW_SIZE[0]//2, y=WINDOW_SIZE[1]//2):
        self.image = pygame.image.load("assets/images/spaceship_player.png")
        self.rect = self.image.get_rect()
        
        self.total_columns = total_columns
        self.velx = 0
        self.vel_mod = 4
        self.column_pos = ceil(total_columns/2)
        self.rect.center = (WINDOW_SIZE[0] * self.column_pos / (total_columns + 1), y)
        
    def update(self):
        self.rect.x += self.velx
        
    def move(self, direction):
        print(self.column_pos)
        if direction == 'right':
            self.column_pos += 1
        elif direction == 'left':
            self.column_pos -= 1
        else:
            raise Exception(f"Invalid direction {direction}")
        
        self.rect.centerx = WINDOW_SIZE[0] * self.column_pos / (self.total_columns + 1)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
