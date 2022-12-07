import pygame
import sys, os, time, csv
from .common.settings import *
from .common.ui_utils import *
from .player import Player
from .asteroid import Asteroid
from .mqtt.client import client as mqtt_client
from .serial.connection import ser


fim_de_jogo = False

FPS = 90
ser.open()
user = 'grupo1-bancadaA6'

game_time = {
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

scores = {
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

modo0 = '0'
modo1 = '0'

class Game:

    def on_message_fim_de_jogo(self, client, userdata, msg):
        global fim_de_jogo
        if msg.payload.decode('utf-8') == "1":
            fim_de_jogo = True

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("FPGAsteroids")
        pygame.display.set_icon(pygame.image.load('assets/images/spaceship_icon.png'))
        mqtt_client.on_message = self.on_message_fim_de_jogo             # Vinculo do Callback de mensagem recebida
        mqtt_client.loop_start()

    def game_loop(self):
        self.screen_name = 'game_loop'
        done = False
        while not done:
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    self.quit()
                    
                if event.type == pygame.KEYDOWN:
                    # Movement events
                    if event.key == pygame.K_a:
                        if self.mode == 3:
                            ser.write('a'.encode())
                        else:
                            self.player.move('left')
                    if event.key == pygame.K_d:
                        if self.mode == 3:
                            ser.write('d'.encode())
                        else:
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
                        self.stop = time.time()
                        game_time[self.mode] += self.stop - self.start
                        mqtt_client.publish(user+'/E5', '1')
                        pygame.time.set_timer(self.cancel_timer, 2000)
                        self.start_game(mode=self.mode)
                        
                    # if event.key == pygame.K_q:
                    #     pygame.quit()
                    #     sys.exit()
                if event.type == self.initial_timer:
                    mqtt_client.publish(user+'/E0', '0')
                    mqtt_client.publish(user+'/E1', '0')
                    mqtt_client.publish(user+'/E3', '0')
                    mqtt_client.publish(user+'/E2', '0')

                if event.type == self.confirm_timer:
                    mqtt_client.publish(user+'/E4', '0')

                # if event.type == self.cancel_timer:
                #     mqtt_client.publish(user+'/E4', '0')


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

        self.initial_timer = pygame.USEREVENT
        self.confirm_timer = pygame.USEREVENT+1
        self.cancel_timer = pygame.USEREVENT+2

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
        
        self.reaction_time = {}

        self.player = Player(self.total_columns, y=WINDOW_SIZE[1]-60)
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
        if self.mode == 1 or self.mode == 3:
            if self.serial_frame_count > 17:
                msg = ser.read(8).decode('utf-8')
                print(msg)
                try:
                    pos = self.pos_to_column[msg[:3]]
                    self.player.move(pos=pos)
                    if msg[4] == '0':
                        dist = 700 - int(msg[4:-1])*(350/25)
                        print(dist)
                        already_exists = False
                        for asteroid in self.asteroids:
                            if pos == asteroid.column_pos:
                                already_exists = True
                                asteroid.move(dist)

                        if not already_exists:
                            self.create_asteroid(pos, y=dist)
    
                        ser.flushInput()
                except:
                    pass
                self.serial_frame_count = 0

        if self.mode == 2 or self.mode == 4:
            try:
                if self.serial_frame_count > 17:
                    self.serial_frame_count = 0

                    if dist := self.dist_to_serial():
                            ser.write(dist.encode())
                            print(dist.encode())
                            pos = ser.read(8).decode('utf-8')[:3]
                            print(pos)
                            if pos:
                                self.player.move(pos=self.pos_to_column[pos])
                    else:
                        if self.mode == 4:
                            ser.write('ooo'.encode())
                            pos = ser.read(8).decode('utf-8')[:3]
                            if pos:
                                self.player.move(pos=self.pos_to_column[pos])
            except:
                print("Sinal impuro")

        self.read_mqtt_msg()
        self.screen_update()
        self.check_lose_state()
                
    def dist_to_serial(self):
        dist = -9999
        temp = -100
        for asteroid in self.asteroids:
            if asteroid.column_pos == self.player.column_pos:
                temp = WINDOW_SIZE[1] - asteroid.rect.centery
                if dist == -9999:
                   dist = temp
                elif temp < dist:
                    dist = temp
            
        dist = int(dist*50/700)
        t_dist = dist

        if dist >= 0:
            dist = str(dist)[::-1]
            dist += '0'
            if t_dist < 10:
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
        global modo0 
        global modo1

        play1_button = Button(self.screen, text="Jogar modo 1", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play2_button = Button(self.screen, text="Jogar modo 2", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 50), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play3_button = Button(self.screen, text="Jogar modo 3", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 150), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play4_button = Button(self.screen, text="Jogar modo 4", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 250), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        
        self.screen_name = 'choose_mode_menu'
        chosen = False
        while not chosen: 
            self.draw_background()
            
            write_text(self.screen, "FPGAsteroids", 70, WHITE, center_pos=(WINDOW_SIZE[0]//2, 150))
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
                            modo0 = '0'
                            modo1 = '0'

                        if play2_button.hovering():
                            self.mode = 2
                            chosen = True
                            modo0 = '1'
                            modo1 = '0'

                        if play3_button.hovering():
                            self.mode = 3
                            chosen = True
                            modo0 = '0'
                            modo1 = '1'

                        if play4_button.hovering():
                            self.mode = 4
                            chosen = True
                            modo0 = '1'
                            modo1 = '1'
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu()

            pygame.display.update()
            self.clock.tick(FPS) 

        mqtt_client.publish(user+'/E5', '0')
        mqtt_client.publish(user+'/E0', '1')
        mqtt_client.publish(user+'/E1', '1')
        mqtt_client.publish(user+'/E3', modo0)
        mqtt_client.publish(user+'/E2', modo1)
        pygame.time.set_timer(self.initial_timer, 2000)
        self.start = time.time()
        self.game_loop()
    
    def main_menu(self):
        play1_button = Button(self.screen, text="Jogar", font_size=50, dim=(450, 100), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))

        self.screen_name = 'main_menu'
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
        self.stop = time.time()
        mqtt_client.publish(user+'/E5', '1')
        game_time[self.mode] += self.stop - self.start
        self.write_game_time()
        ser.close()
        pygame.quit()
        sys.exit()
                
    def check_lose_state(self):
        global fim_de_jogo
        # for asteroid in self.asteroids:
        #     if :#asteroid.rect.centery > WINDOW_SIZE[1]-120 and asteroid.column_pos == self.player.column_pos and asteroid.rect.centery < WINDOW_SIZE[1] - 20:  # Collision line
        if fim_de_jogo == True:
            if self.mode == 2 or self.mode == 4:
                dist = self.dist_to_serial()
                ser.write(dist.encode())
            draw_transparent_rect(self.screen, topleft_pos=(0,0))
            scores[self.mode] = self.score
            self.write_scores()
            self.lose_screen()

    def lose_screen(self):
        global modo0 
        global modo1 
        global fim_de_jogo

        fim_de_jogo = False

        play1_button = Button(self.screen, text="Recomeçar", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        play2_button = Button(self.screen, text="Menu Principal", font_size=40, dim=(400, 80), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100), bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122))
        
        self.screen_name = 'lose_screen'
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
                            mqtt_client.publish(user+'/E0', '1')
                            mqtt_client.publish(user+'/E1', '1')
                            mqtt_client.publish(user+'/E3', modo0)
                            mqtt_client.publish(user+'/E2', modo1)
                            mqtt_client.publish(user+'/E4', '1')
                            pygame.time.set_timer(self.initial_timer, 2000)
                            pygame.time.set_timer(self.confirm_timer, 2000)
                            self.init_game(mode=self.mode)
                            self.game_loop()

                        if play2_button.hovering():
                            self.stop = time.time()
                            game_time[self.mode] += self.stop - self.start
                            mqtt_client.publish(user+'/E4', '1')
                            pygame.time.set_timer(self.confirm_timer, 2000)
                            self.start_game(mode=self.mode)
        
            pygame.display.update()
            self.clock.tick(FPS)     
        
    def start_game(self, mode=0):
        self.init_game(mode=mode)
        mqtt_client.publish(user+'/E5', '1')
        pygame.time.set_timer(self.cancel_timer, 2000)
        self.choose_mode_menu()

    def update_ui(self):
        write_text(self.screen, f"{self.score}", 60, WHITE, center_pos=(WINDOW_SIZE[0]//2, 50))
        write_text(self.screen, f"modo={self.mode}", 14, WHITE, topleft_pos=(5, 5))
        if self.debug:
            write_text(self.screen, f"FPS: {round(self.clock.get_fps())}", 14, WHITE, topleft_pos=(WINDOW_SIZE[0]-70, 5))
            
    def handle_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid.draw(self.screen)
            if asteroid.column_pos == self.player.column_pos and asteroid.rect.centery >= WINDOW_SIZE[1]//2:
                self.reaction_time[asteroid]['time'] += 1/90
                pass
            
            if self.debug:
                pygame.draw.rect(self.screen, RED, asteroid.rect, 1)

            if asteroid.rect.y > WINDOW_SIZE[1]:
                self.asteroids.remove(asteroid)
                self.score += 1
                self.write_reaction_time(self.reaction_time[asteroid])
                del self.reaction_time[asteroid]
        
    def handle_player(self):
        self.player.update()
        self.player.draw(self.screen)
        
        if self.debug:
            pygame.draw.rect(self.screen, YELLOW, self.player.rect, 1)
    
    def create_asteroid(self, column, y=70):
        asteroid = Asteroid(column, self.total_columns, y=y)
        self.reaction_time[asteroid] = {'mode': self.mode, 'time': 0}
        self.asteroids.append(asteroid)
        
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
        write_text(self.screen, "Collision line", 14, (10, 89, 247), topleft_pos=(WINDOW_SIZE[0]-95, WINDOW_SIZE[1]-125))
        pygame.draw.line(self.screen, (10, 89, 247), (0, WINDOW_SIZE[1]-130), (WINDOW_SIZE[0], WINDOW_SIZE[1]-130), 2)
        
        write_text(self.screen, "Evasion line", 14, YELLOW, topleft_pos=(WINDOW_SIZE[0]-90, WINDOW_SIZE[1]//2+5))
        pygame.draw.line(self.screen, YELLOW, (0, WINDOW_SIZE[1]//2), (WINDOW_SIZE[0], WINDOW_SIZE[1]//2), 2)
        
    def write_game_time(self):
        l = [t for t in game_time.values()]
        with open('digital_twin/tempo_de_jogo.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(l)
            
    def write_scores(self):  
        l = [self.mode, self.score]
        with open('digital_twin/pontuacao.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(l)

    def write_reaction_time(self, reaction_time):
        l = [t for t in reaction_time.values()]
        with open('digital_twin/tempo_de_reacao.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(l)
            