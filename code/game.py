import pygame
import sys
from .common.settings import *
from .common.ui_utils import *
from .player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPGAsteroids")
        pygame.display.set_icon(pygame.image.load('assets/images/spaceship_icon.png'))

        self.init_game()
        self.game_loop()
        
    def init_game(self):
        self.total_columns = 5
        self.player = Player(self.total_columns, x=WINDOW_SIZE[0]//2, y=WINDOW_SIZE[1]//2 + 300)
    
    def game_loop(self):
        while True:
            self.screen.fill(NIGHTBLUE)
            
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    # Movement events
                    if event.key == pygame.K_a:
                        self.player.move('left')
                    if event.key == pygame.K_d:
                        self.player.move('right')
                            
                # if event.type == pygame.KEYUP:
                #     # Movement events
                #     if event.key == pygame.K_a:
                #         self.player.velx -= -self.player.vel_mod
                #     if event.key == pygame.K_d:
                #         self.player.velx -= self.player.vel_mod
                
                    
            self.screen_update()
                    
            pygame.display.update()
            self.clock.tick(120)
            
    def screen_update(self):
        self.player.update()
        self.player.draw(self.screen)
        
        self.draw_column_lines()
        
    def draw_column_lines(self):
        for i in range(1, self.total_columns):
            pygame.draw.line(self.screen, WHITE, (WINDOW_SIZE[0] * i / (self.total_columns + 1), 0), (WINDOW_SIZE[0] * i / (self.total_columns + 1), WINDOW_SIZE[1]), 2)