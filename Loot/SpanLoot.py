import pygame
from NoIdeaGamePygame.module import SettingsLoot, ObjectPath


class LootAppearance:
    def __init__(self, screen=True):
        self.Ak_scale = None
        pygame.init()
        self.screen = None
        self.time_spawn_loot = SettingsLoot.TimeSpawn
        self.image_Ak = str(ObjectPath.Ak)
        self.Ak = None

    def spawn_loot(self):
        self.screen = pygame.display.set_mode((1080, 900))
        self.screen.fill((255, 54, 76))
        self.Ak = pygame.image.load(self.image_Ak)
        self.Ak_scale = pygame.transform.scale(self.Ak, (50, 40))
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print('o9234ju5-')

            self.screen.blit(self.Ak_scale, (1, 1))
            pygame.display.flip()


if __name__ == '__main__':
    d = LootAppearance()
    d.spawn_loot()
