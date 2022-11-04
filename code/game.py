import pygame
import sys
from .common.settings import *
from .common.ui_utils import *
from .player import Player
from .asteroid import Asteroid


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPGAsteroids")
        pygame.display.set_icon(pygame.image.load('assets/images/spaceship_icon.png'))
    
    def game_loop(self, mode=1, debug=False):
        done = False
        while not done:
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
                        
                    # Asteroid events
                    if event.key == pygame.K_1:
                        self.create_asteroid(1)
                    if event.key == pygame.K_2:
                        self.create_asteroid(2)
                    if event.key == pygame.K_3:
                        self.create_asteroid(3)
                    if event.key == pygame.K_4:
                        self.create_asteroid(4)
                    if event.key == pygame.K_5:
                        self.create_asteroid(5)
                        
                    if event.key == pygame.K_ESCAPE:
                        # done = True
                        self.main_menu(debug)  # TODO debugar isso
                        
                    if event.key == pygame.K_q:  # TODO remove
                        pygame.quit()
                        sys.exit()
                
            self.check_lose_state()
            self.screen_update(mode, debug)
                    
            pygame.display.update()
            self.clock.tick(120)
            
    def init_game(self):
        self.total_columns = 5
        
        self.player = Player(self.total_columns, y=WINDOW_SIZE[1]-50)
        self.asteroids = []
        
        self.background = pygame.image.load("assets/images/background.png")
        self.background_height = self.background.get_height()
        self.scroll = 0
            
    def screen_update(self, mode, debug):
        self.draw_background()
        self.draw_column_lines()
        self.draw_vision_lines()
        self.update_ui(mode, debug)          
        
        self.handle_player()
        self.handle_asteroids()
        
    def main_menu(self, debug=False):
        play1_button = Button(self.screen, text="Jogar modo 1", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play2_button = Button(self.screen, text="Jogar modo 2", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play3_button = Button(self.screen, text="Jogar modo 3", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 200), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play4_button = Button(self.screen, text="Jogar modo 4", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 300), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        
        while True: 
            self.draw_background()
            
            write_text(self.screen, "FPGAsteroids", 70, WHITE, center_pos=(WINDOW_SIZE[0]//2, 150))
            play1_button.draw()
            play2_button.draw()
            play3_button.draw()
            play4_button.draw()
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play1_button.hovering():
                            self.game_loop(1, debug)

                        if play2_button.hovering():
                            self.game_loop(2, debug)

            pygame.display.update()
            self.clock.tick(120) 

    def check_lose_state(self):
        for asteroid in self.asteroids:
            if asteroid.column_pos == self.player.column_pos and asteroid.rect.centery > WINDOW_SIZE[1]-100:  # Collision line
                self.start_game()

    def start_game(self):
        self.init_game()
        self.main_menu(debug=True)

    def update_ui(self, mode, debug):
        write_text(self.screen, f"modo={mode}", 14, WHITE, topleft_pos=(5, 5))
        if debug:
            write_text(self.screen, f"FPS: {round(self.clock.get_fps())}", 14, WHITE, topleft_pos=(WINDOW_SIZE[0]-70, 5))
            
    def handle_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.draw(self.screen)

            if asteroid.rect.y > WINDOW_SIZE[1]:
                self.asteroids.remove(asteroid)
        
    def handle_player(self):
        self.player.update()
        self.player.draw(self.screen)
    
    def create_asteroid(self, column):
        self.asteroids.append(Asteroid(column, self.total_columns))
        
    def draw_column_lines(self):
        for i in range(1, self.total_columns):
            dx = WINDOW_SIZE[0] / self.total_columns
            pygame.draw.line(self.screen, WHITE, (dx*i - 1, 0), (dx*i, WINDOW_SIZE[1]), 2)
            
    def draw_background(self):
        for i in range(3):
            self.screen.blit(self.background, (0, -(i*self.background_height + self.scroll)))
        
        self.scroll -= 0.5
        if abs(self.scroll) > self.background_height:
            self.scroll = 0
            
    def draw_vision_lines(self):
        write_text(self.screen, "Collision line", 14, RED, topleft_pos=(WINDOW_SIZE[0]-95, WINDOW_SIZE[1]-95))
        pygame.draw.line(self.screen, RED, (0, WINDOW_SIZE[1]-100), (WINDOW_SIZE[0], WINDOW_SIZE[1]-100), 2)
        
        write_text(self.screen, "Evasion line", 14, YELLOW, topleft_pos=(WINDOW_SIZE[0]-90, WINDOW_SIZE[1]//2+5))
        pygame.draw.line(self.screen, YELLOW, (0, WINDOW_SIZE[1]//2), (WINDOW_SIZE[0], WINDOW_SIZE[1]//2), 2)
        