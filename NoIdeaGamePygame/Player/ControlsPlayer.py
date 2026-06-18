import pygame
from NoIdeaGamePygame.module import ControlsPlayer


class Controls:
    def __init__(self):
        self.controls_dict = ControlsPlayer.ControlsPlayer
        self.w = pygame.K_w
        self.s = pygame.K_s


