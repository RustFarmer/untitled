import pygame

from NoIdeaGamePygame.Player.PlayerSettings import Player
from NoIdeaGamePygame.module import SettingsScreenPer


def draw_text(screen, font, text, color, x, y, antialias=True):
    text_surface = font.render(text, antialias, color)
    screen.blit(text_surface, (x, y))
    return text_surface


class ScreenSetting:
    def __init__(self, width, height):
        pygame.init()

        self._width: int = width
        self._height: int = height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill(SettingsScreenPer.Black)
        self.mouse_pos = pygame.mouse.get_pos()

        self.font = pygame.font.SysFont("cosmeticians", 36)
        self.text_settings = self.font.render("Settings", True, (0, 128, 0))

        self.button_width: int = 300
        self.button_height: int = 70
        self.center_x: int = self._width // 2
        self.center_y: int = self._height // 2
        self.gap: int = 5
        self.text_change = self.font.render("Change foreskin", True, (0, 128, 0))
        self.change_button_y: int = self.center_y + self.gap // 2
        self.change_text_rect = self.text_change.get_rect(center=(self.button_width // 2, self.button_height // 2))
        self.change_skin_y: int = 200
        self.settings_text_rect = self.text_settings.get_rect(center=(self.button_width // 2, self.button_height // 2))

        self.change_rect = pygame.Rect(100, self.change_skin_y, self.button_width, self.button_height)
        self.change_surface = pygame.Surface((self.button_width, self.button_height))

        self.event = None
        self.DONE: bool = False

    def draw_button(self, surface, rect, text_rect, text, is_hovered):
        if is_hovered:
            surface.fill((127, 255, 212))
        else:
            surface.fill((200, 200, 200))
        pygame.draw.rect(surface, SettingsScreenPer.Black, surface.get_rect(), 3)
        surface.blit(text, text_rect)
        self.screen.blit(surface, rect)

    def run_settings_menu(self):
        print(self.font, self.screen)
        mouse_pos = pygame.mouse.get_pos()
        Pl = Player(self.screen)
        while not self.DONE:
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.DONE = True
                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    if self.change_rect.collidepoint(self.event.pos):
                        Player(self.screen).change_skin_player()
                        pygame.display.flip()

                if self.change_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.change_surface, (127, 255, 212), (1, 1, 148, 48))

            self.screen.fill(SettingsScreenPer.Black)

            self.draw_button(self.change_surface, self.change_rect, self.change_text_rect,
                             self.text_change, self.change_rect.collidepoint(pygame.mouse.get_pos()))

            self.screen.blit(self.text_settings,
                             (500 - self.text_settings.get_width() // 2,
                              150 - self.text_settings.get_height()))

            Pl.rect_player_in_start_menu(750, 200)

            pygame.display.flip()
