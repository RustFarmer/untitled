import pygame, json
from NoIdeaGamePygame.module import SettingsPlayer, SettingsScreenPer, find_in_json, update_json_value
from NoIdeaGamePygame.Player.Sraw_inventory import Inventory

data = "../settings.json"


def save_position(position):
    update_json_value(data, "Player.position", position)


class Player:
    def __init__(self, screen):
        self.position = None
        self.screen = screen
        self.event = None
        self.start_health = None
        self.health = None
        self.skin_player = None
        self.font = pygame.font.SysFont("cosmeticians", 36)
        self.x = SettingsPlayer.PositionX
        self.y = SettingsPlayer.PositionY
        self.width = SettingsPlayer.Width_player
        self.height = SettingsPlayer.Height_player
        self.speed = SettingsPlayer.Speed
        self.scale_move = SettingsPlayer.Scale_move
        self.PositionHealthPoint_X, self.PositionHealthPoint_Y = SettingsPlayer.PositionHealthPoint
        self.PositionHealthPoint_width, self.PositionHealthPoint_height = SettingsPlayer.PositionHealthPoint_width_height

    def loading_skin_player(self) -> list:
        self.skin_player = SettingsPlayer.skin_ust
        self.skin_player = find_in_json(data, "Skin", self.skin_player)
        return self.skin_player

    def change_skin_player(self) -> list:
        print('28903h450')
        with open(data, 'r', encoding='utf-8') as f:
            config = json.load(f)
        available_skins = config.get("Skin", {})
        if not available_skins:
            print("No skins available")
            return self.skin_player

        current_skin_name = SettingsPlayer.skin_ust
        skin_names = list(available_skins.keys())
        if current_skin_name not in skin_names:
            new_skin_name = skin_names[0]
        else:
            idx = skin_names.index(current_skin_name)
            new_skin_name = skin_names[(idx + 1) % len(skin_names)]

        update_json_value(data, "Player.skin_ust", new_skin_name)
        SettingsPlayer.skin_ust = new_skin_name
        self.loading_skin_player()
        return self.skin_player

    def change_health_point(self, damage: int) -> int:
        self.start_health = SettingsPlayer.Health
        self.health = self.start_health - damage
        return self.health

    def update(self, obstacles=None):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        # if keys[pygame.K_w]:
        #     dy -= self.speed
        # if keys[pygame.K_s]:
        #     dy += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        if obstacles:
            self.x += dx
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for rect in obstacles:
                if player_rect.colliderect(rect):
                    if dx > 0:
                        self.x = rect.left - self.width
                    elif dx < 0:
                        self.x = rect.right

            self.y += dy
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for rect in obstacles:
                if player_rect.colliderect(rect):
                    if dy > 0:
                        self.y = rect.top - self.height
                    elif dy < 0:
                        self.y = rect.bottom
        else:
            self.x += dx
            self.y += dy

        screen_width = SettingsScreenPer.width
        screen_height = SettingsScreenPer.height
        self.x = max(0, min(self.x, screen_width - self.width))
        self.y = max(0, min(self.y, screen_height - self.height))

        self.position = [self.x, self.y]

        if keys[pygame.K_TAB]:
            Inventory().draw_inventory()
        # print(self.position)
        return self.position

    def display_health_point(self):
        text_hp = self.font.render("HP", True, (0, 128, 0))
        self.screen.blit(text_hp, (self.PositionHealthPoint_X, self.PositionHealthPoint_Y + 15))
        pygame.draw.rect(self.screen, SettingsPlayer.ColorHealthPoint,
                         pygame.Rect(self.PositionHealthPoint_X, self.PositionHealthPoint_Y,
                                     self.PositionHealthPoint_width, self.PositionHealthPoint_height))

    def rect_player(self):
        return pygame.draw.rect(self.screen, self.skin_player,
                                (self.x, self.y, self.width, self.height))

    def rect_player_in_start_menu(self, x, y):
        self.loading_skin_player()
        text_skin = self.font.render("foreskin", True, (0, 128, 0))
        self.screen.blit(text_skin, (x - text_skin.get_width() // 2 + 30, y - 40))

        pygame.draw.rect(self.screen, self.skin_player, (x, y, self.width, self.height))

    def redy_player(self):
        self.loading_skin_player()
        self.rect_player()
        self.display_health_point()

    def get_position(self) -> dict:
        self.update()
        print(self.position)
        return self.position
