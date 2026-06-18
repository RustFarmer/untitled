import pygame
from NoIdeaGamePygame.Word.generationWord.GenerationWordMain import GenerationWord
from NoIdeaGamePygame.module import SettingsScreenPer, SettingsWeapon
from NoIdeaGamePygame.Player.PlayerSettings import Player, save_position
from NoIdeaGamePygame.Player.WeaponShut import Bullet


class GameScreen:
    def __init__(self):
        self._width: int = SettingsScreenPer.width
        self._height: int = SettingsScreenPer.height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.word = GenerationWord(self.screen)
        self.event = None
        self.DONE = False
        self.bullets = []
        self.last_shot_time = 0  # для контроля частоты стрельбы

    def game_run(self):
        player = Player(self.screen)
        player.redy_player()
        self.word.assembling_the_world()
        pygame.display.flip()

        obstacles = self.word.get_all_collision_rects()

        while not self.DONE:
            # Обработка событий (закрытие окна, ESC и т.д.)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_position(player.update(obstacles))
                    self.DONE = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    save_position(player.update(obstacles))
                    self.DONE = True

            # ----- ОТДЕЛЬНО ОБРАБАТЫВАЕМ СТРЕЛЬБУ (по удержанию ЛКМ) -----
            left_pressed = pygame.mouse.get_pressed()[0]
            current_time = pygame.time.get_ticks()

            if left_pressed:
                # Проверяем, прошло ли достаточно времени с последнего выстрела
                if current_time - self.last_shot_time >= SettingsWeapon.FireRate:
                    # Создаём пулю
                    bullet_width = SettingsWeapon.with_Ak
                    bullet_height = SettingsWeapon.height_ak
                    speed = SettingsWeapon.BulletSpeed
                    color = SettingsWeapon.ColorBullet

                    # Начальная позиция (центр игрока)
                    start_x = player.x + player.width // 2 - bullet_width // 2
                    start_y = player.y + player.height // 2 - bullet_height // 2

                    # Направление на курсор мыши
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - (player.x + player.width // 2)
                    dy = mouse_y - (player.y + player.height // 2)
                    length = (dx**2 + dy**2) ** 0.5

                    if length != 0:
                        vx = (dx / length) * speed
                        vy = (dy / length) * speed
                    else:
                        vx, vy = 0, -speed

                    bullet = Bullet(start_x, start_y, color, bullet_width, bullet_height, vx, vy)
                    self.bullets.append(bullet)

                    # Обновляем время последнего выстрела
                    self.last_shot_time = current_time

            # ----- Обновление игрока и пуль -----
            player.update(obstacles)

            for bullet in self.bullets:
                bullet.update()

            # Удаляем пули, вышедшие за экран
            screen_width = SettingsScreenPer.width
            screen_height = SettingsScreenPer.height
            self.bullets = [b for b in self.bullets if not b.is_off_screen(screen_width, screen_height)]

            # ----- Отрисовка -----
            self.screen.fill((0, 0, 0))
            self.word.assembling_the_world()
            player.rect_player()
            player.display_health_point()

            for bullet in self.bullets:
                bullet.draw(self.screen)

            pygame.display.flip()