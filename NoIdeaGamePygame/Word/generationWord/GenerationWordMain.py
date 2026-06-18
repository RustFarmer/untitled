import pygame
from NoIdeaGamePygame.module import SettingsScreenPer


class GenerationWord:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill(SettingsScreenPer.Black)

    def first_layer(self):
        return pygame.draw.rect(self.screen, SettingsScreenPer.Brown,
                                pygame.Rect(SettingsScreenPer.FirstSetting_x,
                                            SettingsScreenPer.FirstSetting_y,
                                            1080, 100))

    def second_layer(self):
        return pygame.draw.rect(self.screen, SettingsScreenPer.White,
                                pygame.Rect(SettingsScreenPer.FirstSetting_x,
                                            SettingsScreenPer.FirstSetting_y - 100,
                                            1080, 100))

    # def generation_layer(self):
        # for x in range(12):
            # pygame.draw.rect(self.screen, )

    def third_layer(self):
        pass

    def others_layer(self):
        pass

    def assembling_the_world(self):
        self.first_layer()
        self.second_layer()
        self.third_layer()
        self.others_layer()

    def get_first_rect(self) -> pygame.Rect:
        return pygame.Rect(SettingsScreenPer.FirstSetting_x,
                           SettingsScreenPer.FirstSetting_y,
                           1080, 100)

    def get_second_rect(self) -> pygame.Rect:
        return pygame.Rect(SettingsScreenPer.FirstSetting_x,
                           SettingsScreenPer.FirstSetting_y - 100,
                           1080, 100)

    def get_all_collision_rects(self) -> list:
        rects = []
        r1 = self.get_first_rect()
        if r1.width > 0 and r1.height > 0:
            rects.append(r1)
        r2 = self.get_second_rect()
        if r2.width > 0 and r2.height > 0:
            rects.append(r2)
        return rects
