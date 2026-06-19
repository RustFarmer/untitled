import math

import pygame, random
from NoIdeaGamePygame.Word.generationWord.GenerationWordMain import GenerationWord
from NoIdeaGamePygame.module import SettingsScreenPer, SettingsWeapon, SettingsSound, SettingsLoot, HotSlotInventory, \
    FPS, SettingEnemy, SettingsAmmo
from NoIdeaGamePygame.Player.PlayerSettings import Player, save_position
from NoIdeaGamePygame.Player.WeaponShut import Weapon, Bullet, TimeStopEffect
from NoIdeaGamePygame.Enemy.Movement_Enemy import MovementEnemy


class GameScreen:
    def __init__(self):
        pygame.mixer.init()
        self.FPS = FPS.Fps
        self._width = SettingsScreenPer.width
        self._height = SettingsScreenPer.height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.word = GenerationWord(self.screen)
        self.event = None
        self.DONE = False
        self.bullets = []
        self.last_shot_time = 0

        self.enemies = []
        self.time_stop_center = (0, 0)

        self.time_stop_last_used = -10000
        self.time_stop_cooldown_time = SettingsAmmo.TimeStopCooldown

        self.shoot_sound_AK = None
        try:
            self.shoot_sound_AK = pygame.mixer.Sound(SettingsSound.ShootSound_Ak)
            self.shoot_sound_M416 = pygame.mixer.Sound(SettingsSound.ShootSound_m416)
            time_stop_sound = pygame.mixer.Sound(SettingsSound.TimeStop_first)
            time_stop_sound.set_volume(SettingsSound.TimeStop_first_volume)
            self.time_stop = TimeStopEffect(time_stop_sound)
        except Exception as e:
            print(f"Не удалось загрузить звук: {e}")
            self.time_stop = TimeStopEffect(None)

    def apply_time_stop_effect(self, current_time):
        if self.time_stop.active:
            for enemy in self.enemies:
                enemy_center_x = enemy.x + SettingEnemy.width_pigeon // 2
                enemy_center_y = enemy.y + SettingEnemy.height_pigeon // 2
                dist = ((self.time_stop_center[0] - enemy_center_x) ** 2 +
                        (self.time_stop_center[1] - enemy_center_y) ** 2) ** 0.5
                if dist <= self.time_stop.radius:
                    enemy.freeze(current_time)

    def game_run(self):
        player = Player(self.screen)
        player.redy_player()
        self.word.assembling_the_world()
        pygame.display.flip()
        obstacles = self.word.get_all_collision_rects()
        clock = pygame.time.Clock()
        item_name = SettingsLoot.InventoryCache[0]
        player.change_weapon(item_name)

        for _ in range(1):
            enemy = MovementEnemy(
                self.screen,
                random.randint(100, 900),
                random.randint(100, 700),
                "pigeon"
            )
            self.enemies.append(enemy)

        while not self.DONE:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_position(player.update(obstacles))
                    self.DONE = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    save_position(player.update(obstacles))
                    self.DONE = True
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        slot_index = event.key - pygame.K_1
                        inventory = SettingsLoot.InventoryCache
                        if slot_index < len(inventory) and slot_index < HotSlotInventory.CountSlotHotSlot:
                            item_name = inventory[slot_index]
                            player.change_weapon(item_name)

                    if event.key == pygame.K_r:
                        player.reload_weapon()

            left_pressed = pygame.mouse.get_pressed()[0]
            current_time = pygame.time.get_ticks()
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if left_pressed:
                if item_name == "ak":
                    if player.has_ammo() and current_time - self.last_shot_time >= SettingsWeapon.FireRate_Ak:
                        player.consume_ammo()

                        bullet_width = SettingsWeapon.with_Ak
                        bullet_height = SettingsWeapon.height_ak
                        start_x = player.x + player.width // 2 - bullet_width // 2
                        start_y = player.y + player.height // 2 - bullet_height // 2
                        dx = mouse_x - (player.x + player.width // 2)
                        dy = mouse_y - (player.y + player.height // 2)
                        Weapon(start_x, start_y, dx, dy, self.bullets, bullet_width, bullet_height,
                               self.shoot_sound_AK, current_time)
                        self.last_shot_time = current_time

                if item_name == "m416":
                    if player.has_ammo() and current_time - self.last_shot_time >= SettingsWeapon.FireRate_M416:
                        player.consume_ammo()

                        bullet_width = SettingsWeapon.with_Ak
                        bullet_height = SettingsWeapon.height_ak
                        start_x = player.x + player.width // 2 - bullet_width // 2
                        start_y = player.y + player.height // 2 - bullet_height // 2
                        dx = mouse_x - (player.x + player.width // 2)
                        dy = mouse_y - (player.y + player.height // 2)
                        Weapon(start_x, start_y, dx, dy, self.bullets, bullet_width, bullet_height,
                               self.shoot_sound_M416, current_time)
                        self.last_shot_time = current_time

                if item_name == "timeStopClock":
                    if current_time - self.time_stop_last_used >= self.time_stop_cooldown_time:
                        self.time_stop_center = (player.x + player.width // 2, player.y + player.height // 2)
                        self.time_stop.activate()
                        self.time_stop_last_used = current_time

            player.update(obstacles)
            for bullet in self.bullets:
                bullet.update()
            screen_width = SettingsScreenPer.width
            screen_height = SettingsScreenPer.height
            self.bullets = [b for b in self.bullets if not b.is_off_screen(screen_width, screen_height)]

            self.time_stop.update(current_time)
            self.apply_time_stop_effect(current_time)

            remaining_cooldown = max(0, self.time_stop_cooldown_time - (current_time - self.time_stop_last_used))

            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.update_weapon_angle((mouse_x, mouse_y))

            self.screen.fill((0, 0, 0))
            player.hot_slot_inventory(time_stop_cooldown_remaining=remaining_cooldown)

            self.word.assembling_the_world()
            for enemy in self.enemies:
                enemy.redy_enemy(current_time, (random.randint(0, 500), random.randint(0, 900)))


            player.rect_player()
            player.display_health_point()
            player.draw_weapon(self.screen)
            player.loading_skin_player()

            center = (player.x + player.width // 2, player.y + player.height // 2)
            self.time_stop.draw(self.screen, center)

            for bullet in self.bullets:
                bullet.draw(self.screen)

            pygame.display.flip()