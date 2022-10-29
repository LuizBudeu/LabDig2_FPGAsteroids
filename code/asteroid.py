from .common.settings import *
from .common.ui_utils import *


class Asteroid:
    def __init__(self, x=WINDOW_SIZE[0]//2, y=WINDOW_SIZE[1]//2):
        self.image = pygame.image.load("assets/images/asteroid.png")
        self.rect = self.image.get_rect()
        
        self.rect.center = (x, y)