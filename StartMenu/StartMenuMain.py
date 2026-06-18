import pygame
from NoIdeaGamePygame.module import SettingsScreenPer
from NoIdeaGamePygame.GameScreen.GameScreenMain import GameScreen
from NoIdeaGamePygame.SettingsScreen.SettingsScreenMain import ScreenSetting
from NoIdeaGamePygame.Player.PlayerSettings import Player


class StartMenu:
    def __init__(self, width, height):
        pygame.init()

        self._width: int = width
        self._height: int = height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill(SettingsScreenPer.Black)
        self.font = pygame.font.SysFont("cosmeticians", 36)
        self.text_play = self.font.render("Play", True, (0, 128, 0))
        self.text_settings = self.font.render("Settings", True, (0, 128, 0))

        button_width: int = 200
        button_height: int = 60
        gap: int = 5

        center_x: int = self._width // 2
        center_y: int = self._height // 2

        play_y: int = center_y - button_height - gap // 2
        self.play_rect = pygame.Rect(center_x - button_width // 2, play_y, button_width, button_height)
        self.play_surface = pygame.Surface((button_width, button_height))

        settings_y: int = center_y + gap // 2
        self.settings_rect = pygame.Rect(center_x - button_width // 2, settings_y, button_width, button_height)
        self.settings_surface = pygame.Surface((button_width, button_height))

        self.play_text_rect = self.text_play.get_rect(center=(button_width // 2, button_height // 2))
        self.settings_text_rect = self.text_settings.get_rect(center=(button_width // 2, button_height // 2))

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

    def run_start_menu(self):
        while not self.DONE:

            Pl = Player(self.screen)
            mouse_pos = pygame.mouse.get_pos()

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.DONE = True

                if self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_z:
                        self.DONE = True

                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    if self.play_rect.collidepoint(self.event.pos):
                        gm = GameScreen()
                        gm.game_run()
                    elif self.settings_rect.collidepoint(self.event.pos):
                        settingsmenu = ScreenSetting(self._width, self._height)
                        settingsmenu.run_settings_menu()
                        print("Settings button clicked!")

            self.screen.fill(SettingsScreenPer.Black)

            self.draw_button(self.play_surface, self.play_rect, self.play_text_rect,
                             self.text_play, self.play_rect.collidepoint(mouse_pos))

            self.draw_button(self.settings_surface, self.settings_rect, self.settings_text_rect,
                             self.text_settings, self.settings_rect.collidepoint(mouse_pos))

            Pl.rect_player_in_start_menu(900, 700)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    St = StartMenu(SettingsScreenPer.width, SettingsScreenPer.height)
    St.run_start_menu()
