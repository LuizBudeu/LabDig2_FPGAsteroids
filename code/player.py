from math import ceil
from .common.settings import *
from .common.ui_utils import *


class Player:
    def __init__(self, total_columns, x=WINDOW_SIZE[0]//2, y=WINDOW_SIZE[1]//2):
        self.image = pygame.image.load("assets/images/spaceship_player.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.total_columns = total_columns
        self.velx = 0
        self.vel_mod = 4
        self.column_pos = ceil(total_columns/2)
        self.rect.center = (WINDOW_SIZE[0] * self.column_pos / (total_columns + 1), y)
        self.posses = {i: int(WINDOW_SIZE[0]//total_columns * (i-0.5)) for i in range(1, total_columns+1)}
        print(self.posses)
        
    def update(self):
        self.rect.x += self.velx
        
    def move(self, direction):
        if direction == 'right' and self.column_pos < self.total_columns:
            self.column_pos += 1
        elif direction == 'left' and self.column_pos > 1:
            self.column_pos -= 1
        
        self.rect.centerx = self.posses[self.column_pos]        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
