import pygame
from NoIdeaGamePygame.generationWord.GenerationWordMain import GenerationWord
from NoIdeaGamePygame.module import SettingsScreenPer
from NoIdeaGamePygame.Player.PlayerSettings import Player, save_position


class GameScreen:
    def __init__(self):
        self._width: int = SettingsScreenPer.width
        self._height: int = SettingsScreenPer.height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.word = GenerationWord(self.screen)
        self.event = None
        self.DONE = False


    def game_run(self):
        player = Player(self.screen)
        player.redy_player()
        self.word.assembling_the_world()
        pygame.display.flip()

        while not self.DONE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_position(player.update())
                    self.DONE = True
            player.update()

            self.screen.fill((0, 0, 0))
            self.word.assembling_the_world()
            player.rect_player()
            player.display_health_point()
            pygame.display.flip()
