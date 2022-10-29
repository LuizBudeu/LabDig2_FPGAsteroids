import pygame
from .settings import *


class Button:
    def __init__(self, screen, text="Insert text here", font_size=20, dim=(200, 100), center_pos=(100, 50), topleft_pos=None, bg_color=(154, 171, 170), bg_tocolor=(110, 122, 122)):
        self.font = pygame.font.Font("freesansbold.ttf", font_size)

        self.screen = screen
        self.text = text
        self.bg_color = bg_color
        self.bg_tocolor = bg_tocolor

        if not topleft_pos:
            self.rect = pygame.Rect(
                center_pos[0] - dim[0]//2, center_pos[1] - dim[1]//2, dim[0], dim[1])
        else:
            self.rect = pygame.Rect(
                topleft_pos[0], topleft_pos[1], dim[0], dim[1])

    def draw(self):
        mx, my = get_mouse_pos()
        if self.hovering():
            pygame.draw.rect(self.screen, self.bg_tocolor, self.rect)
        else:
            pygame.draw.rect(self.screen, self.bg_color, self.rect)

        text_surface = self.font.render(self.text, True, DARKGRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def hovering(self):
        mx, my = get_mouse_pos()
        if self.rect.collidepoint(mx, my):
            return True
        return False


def write_text(screen, text='Insert text here', font_size=50, color=(0, 0, 0), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), topleft_pos=None):
    font = pygame.font.Font("freesansbold.ttf", font_size)
    text_surf = font.render(text, True, color)
    if not topleft_pos:
        text_rect = text_surf.get_rect(center=center_pos)
    else:
        text_rect = text_surf.get_rect(topleft=topleft_pos)
    screen.blit(text_surf, text_rect)


def draw_transparent_rect(screen, center_pos=(100, 100), topleft_pos=None, dim=WINDOW_SIZE, color=(255, 255, 255)):
    s = pygame.Surface(dim)  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill(color)           # this fills the entire surface

    if topleft_pos:
        screen.blit(s, topleft_pos)
    else:
        screen.blit(s, (center_pos[0]-dim[0]//2, center_pos[1]-dim[1]//2))


def get_mouse_pos():
    return pygame.mouse.get_pos()


def draw_fading_rect(screen, x, y, width, height, color, time):
    w = width-time
    h = height-time
    if w > 0 and h > 0:
        pygame.draw.rect(screen, color, (x+time/2, y+time/2, w, h), 3)


def pprint_matrix(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
