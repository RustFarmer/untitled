from NoIdeaGamePygame.module import SettingEnemy
import pygame


class MovementEnemy:
    images = []
    current_image_index = 0
    last_switch_time = 0
    loaded = False
    switch_interval = 100

    def __init__(self, screen, x, y, name_enemy):
        self.x, self.y = x, y
        self.position = [self.x, self.y]
        self.screen = screen
        self.name_enemy = name_enemy
        self.frozen_until = 0
        self.speed = 3

        if not MovementEnemy.loaded:
            self.load_images()
            MovementEnemy.loaded = True

    def load_images(self):
        if self.name_enemy == 'pigeon':
            try:
                for path in SettingEnemy.skin_PATH:
                    img = pygame.image.load(path)
                    MovementEnemy.images.append(img)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                if not MovementEnemy.images:
                    MovementEnemy.images.append(pygame.Surface((50, 50)))

    def freeze(self, current_time):
        self.frozen_until = current_time + 10000

    def redy_enemy(self, current_time, player_center=None):
        if not MovementEnemy.images:
            return

        if current_time - MovementEnemy.last_switch_time > MovementEnemy.switch_interval:
            MovementEnemy.current_image_index = (MovementEnemy.current_image_index + 1) % len(MovementEnemy.images)
            MovementEnemy.last_switch_time = current_time

        if current_time >= self.frozen_until and player_center:
            dx = player_center[0] - (self.x + SettingEnemy.width_pigeon // 2)
            dy = player_center[1] - (self.y + SettingEnemy.height_pigeon // 2)
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist > 1:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
            self.position = [self.x, self.y]

        img = MovementEnemy.images[MovementEnemy.current_image_index]
        scaled_img = pygame.transform.scale(img, (SettingEnemy.width_pigeon, SettingEnemy.height_pigeon))

        if current_time < self.frozen_until:
            frozen_surface = scaled_img.copy()
            frozen_surface.fill((0, 0, 255, 128), None, pygame.BLEND_RGBA_MULT)
            self.screen.blit(frozen_surface, self.position)
        else:
            self.screen.blit(scaled_img, self.position)
