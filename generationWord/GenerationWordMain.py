import pygame
from NoIdeaGamePygame.module import SettingsScreenPer


class GenerationWord:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(SettingsScreenPer.Black)

        print(SettingsScreenPer.Black)

    def first_layer(self):
        pygame.draw.rect(self.screen, SettingsScreenPer.Brown, pygame.Rect(SettingsScreenPer.FirstSetting_x, SettingsScreenPer.FirstSetting_y,
                                                                           1080, 100))

    def second_layer(self):
        pygame.draw.rect(self.screen, SettingsScreenPer.White,
                         pygame.Rect(SettingsScreenPer.FirstSetting_x, SettingsScreenPer.FirstSetting_y - 100,
                                     1080, 100))

    def third_layer(self):
        pass

    def others_layer(self):
        pass

    def assembling_the_world(self):
        self.first_layer()
        self.second_layer()
        self.third_layer()
        self.others_layer()




