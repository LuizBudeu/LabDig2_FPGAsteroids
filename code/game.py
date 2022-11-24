import pygame
import sys, os, time
from .common.settings import *
from .common.ui_utils import *
from .player import Player
from .asteroid import Asteroid
from .mqtt.client import client as mqtt_client
from .serial.connection import ser


FPS = 90
ser.open()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPGAsteroids")
        pygame.display.set_icon(pygame.image.load('assets/images/spaceship_icon.png'))
    
    def game_loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    self.quit()
                    
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
                        self.main_menu()
                        
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            if self.mqtt_msg == 'a':
                self.player.move('left')
            if self.mqtt_msg == 'd':
                self.player.move('right')

            if self.mqtt_msg is not None:
                self.mqtt_msg = None
                os.remove(self.mqtt_msg_path)
            self.serial_frame_count += 1
            self.update()
                    
            pygame.display.update()
            self.clock.tick(FPS)
            
    def init_game(self, mode=0):
        self.serial_frame_count = 0
        ser.flushInput()

        self.total_columns = 5
        self.score = 0
        self.mode = mode
        self.debug = False
        self.pos_to_column = {
            '020': 1,
            '040': 2,
            '060': 3,
            '080': 4,
            '100': 5
        }
        
        self.player = Player(self.total_columns, y=WINDOW_SIZE[1]-50)
        self.asteroids = []
        
        self.background = pygame.image.load("assets/images/background.png")
        self.background_height = self.background.get_height()
        self.scroll = 0

        self.mqtt_msg = None
        self.mqtt_msg_path = 'code/mqtt/msg.txt'
        if os.path.exists(self.mqtt_msg_path):
            os.remove(self.mqtt_msg_path)

    def screen_update(self):
        self.draw_background()
        self.draw_column_lines()
        self.draw_vision_lines()
        self.update_ui()          

        self.handle_player()
        self.handle_asteroids()

    def update(self):
        if self.mode == 1:
            if self.serial_frame_count > 17:
                msg = ser.read(8).decode('utf-8')
                print(msg)
                if msg[4] == '0':
                    pos = self.pos_to_column[msg[:3]]
                    dist = 700 - int(msg[4:-1])*(700/50)
                    print(dist)
                    already_exists = False
                    for asteroid in self.asteroids:
                        if pos == asteroid.column_pos:
                            already_exists = True
                            asteroid.move(dist)

                    if not already_exists:
                        self.asteroids.append(Asteroid(pos, self.total_columns, y=dist))

                    self.player.move(pos=pos)
                    self.serial_frame_count = 0
                    ser.flushInput()

        if self.mode == 2: 
            if dist := self.dist_to_serial():
                if self.serial_frame_count > 17:
                    ser.write(dist.encode())
                    print(dist.encode())
                    pos = ser.read(8).decode('utf-8')[:3]
                    print(pos)
                    if pos:
                        self.player.move(pos=self.pos_to_column[pos])
                    self.serial_frame_count = 0

        self.read_mqtt_msg()
        self.screen_update()
        self.check_lose_state()
                
    def dist_to_serial(self):
        dist = -9999
        for asteroid in self.asteroids:
            if asteroid.column_pos == self.player.column_pos:
                dist = WINDOW_SIZE[1] - asteroid.rect.centery
            
        dist = int(dist*50/700)

        if dist >= 0:
            dist = str(dist)[::-1]
            dist += '0'
            return dist
        return None

    def read_mqtt_msg(self):
        try:
            with open(self.mqtt_msg_path, 'r') as f:
                self.mqtt_msg = f.read()
        except FileNotFoundError:
            pass
        
    def choose_mode_menu(self):
        play1_button = Button(self.screen, text="Jogar modo 1", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play2_button = Button(self.screen, text="Jogar modo 2", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 50), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play3_button = Button(self.screen, text="Jogar modo 3", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 150), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play4_button = Button(self.screen, text="Jogar modo 4", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 250), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        
        chosen = False
        while not chosen: 
            self.draw_background()
            
            write_text(self.screen, "Escolher modo", 70, WHITE, center_pos=(WINDOW_SIZE[0]//2, 150))
            play1_button.draw()
            play2_button.draw()
            play3_button.draw()
            play4_button.draw()
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play1_button.hovering():
                            self.mode = 1
                            chosen = True

                        if play2_button.hovering():
                            self.mode = 2
                            chosen = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            pygame.display.update()
            self.clock.tick(FPS) 
        
        self.game_loop()
    
    def main_menu(self):
        play1_button = Button(self.screen, text="Jogar", font_size=50, dim=(450, 100), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))

        while True: 
            self.draw_background()
            
            write_text(self.screen, "FPGAsteroids", 70, WHITE, center_pos=(WINDOW_SIZE[0]//2, 250))
            play1_button.draw()
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play1_button.hovering():
                            self.choose_mode_menu()

            pygame.display.update()
            self.clock.tick(FPS) 

    def quit(self):
        ser.close()
        pygame.quit()
        sys.exit()
                
    def check_lose_state(self):
        for asteroid in self.asteroids:
            if asteroid.rect.centery > WINDOW_SIZE[1]-140 and asteroid.column_pos == self.player.column_pos:  # Collision line
                draw_transparent_rect(self.screen, topleft_pos=(0,0))
                self.lose_screen()

    def lose_screen(self):
        play1_button = Button(self.screen, text="Recomeçar", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play2_button = Button(self.screen, text="Menu Principal", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        
        chosen = False
        while not chosen:             
            write_text(self.screen, "Você perdeu!", 70, WHITE, center_pos=(WINDOW_SIZE[0]//2, 150))
            play1_button.draw()
            play2_button.draw()
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play1_button.hovering():
                            self.init_game(mode=self.mode)
                            self.game_loop()

                        if play2_button.hovering():
                            self.start_game()

            pygame.display.update()
            self.clock.tick(FPS)     
        
    def start_game(self):
        self.init_game()
        self.main_menu()

    def update_ui(self):
        write_text(self.screen, f"{self.score}", 60, WHITE, center_pos=(WINDOW_SIZE[0]//2, 50))
        write_text(self.screen, f"modo={self.mode}", 14, WHITE, topleft_pos=(5, 5))
        if self.debug:
            write_text(self.screen, f"FPS: {round(self.clock.get_fps())}", 14, WHITE, topleft_pos=(WINDOW_SIZE[0]-70, 5))
            
    def handle_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.draw(self.screen)
            
            if self.debug:
                pygame.draw.rect(self.screen, RED, asteroid.rect, 1)

            if asteroid.rect.y > WINDOW_SIZE[1]:
                self.asteroids.remove(asteroid)
                self.score += 1
        
    def handle_player(self):
        self.player.update()
        self.player.draw(self.screen)
        
        if self.debug:
            pygame.draw.rect(self.screen, YELLOW, self.player.rect, 1)
    
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
        write_text(self.screen, "Collision line", 14, RED, topleft_pos=(WINDOW_SIZE[0]-145, WINDOW_SIZE[1]-145))
        pygame.draw.line(self.screen, RED, (0, WINDOW_SIZE[1]-140), (WINDOW_SIZE[0], WINDOW_SIZE[1]-140), 2)
        
        write_text(self.screen, "Evasion line", 14, YELLOW, topleft_pos=(WINDOW_SIZE[0]-90, WINDOW_SIZE[1]//2+5))
        pygame.draw.line(self.screen, YELLOW, (0, WINDOW_SIZE[1]//2), (WINDOW_SIZE[0], WINDOW_SIZE[1]//2), 2)
        