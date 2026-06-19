import pygame, json, math
from NoIdeaGamePygame.module import SettingsPlayer, SettingsScreenPer, find_in_json, update_json_value, ObjectPath, \
    HotSlotInventory, SettingsLoot, GetKey, SettingsAmmo
from NoIdeaGamePygame.Player.Draw_inventory import Inventory

data = "../settings.json"


def save_position(position):
    update_json_value(data, "Player.position", position)


class Player:
    def __init__(self, screen):
        self.slot_rect = None
        self.position = None
        self.screen = screen
        self.event = None
        self.start_health = None
        self.health = None
        self.skin_player = None
        self.current_weapon_name = None
        self.weapon_image = None
        self.path = None

        self.load_default_weapon()
        self.font = pygame.font.SysFont("cosmeticians", 36)
        self.ammo_font = pygame.font.SysFont("cosmeticians", 14)

        self.x = SettingsPlayer.PositionX
        self.y = SettingsPlayer.PositionY
        self.width = SettingsPlayer.Width_player
        self.height = SettingsPlayer.Height_player
        self.speed = SettingsPlayer.Speed
        self.scale_move = SettingsPlayer.Scale_move
        self.PositionHealthPoint_X, self.PositionHealthPoint_Y = SettingsPlayer.PositionHealthPoint
        self.PositionHealthPoint_width, self.PositionHealthPoint_height = SettingsPlayer.PositionHealthPoint_width_height

        try:
            raw_image = pygame.image.load(ObjectPath.M416)
            weapon_size = (100, 60)
            self.weapon_image = pygame.transform.scale(raw_image, weapon_size)
        except (pygame.error, FileNotFoundError):
            print(f"{ObjectPath.Ak}")
            self.weapon_image = pygame.Surface((30, 30))
            self.weapon_image.fill((255, 0, 255))
        self.weapon_angle = 0
        self.is_moving = False

        self.weapons_ammo = {
            "ak": {
                "ammo": SettingsAmmo.AkMaxAmmo,
                "magazines": SettingsAmmo.AkInitialMagazines,
                "max_ammo": SettingsAmmo.AkMaxAmmo
            },
            "m416": {
                "ammo": SettingsAmmo.M416MaxAmmo,
                "magazines": SettingsAmmo.M416InitialMagazines,
                "max_ammo": SettingsAmmo.M416MaxAmmo
            },
            "timeStopClock": {
                "ammo": float('inf'),
                "magazines": float('inf'),
                "max_ammo": float('inf')
            }
        }
        self.current_weapon_stats = self.weapons_ammo.get(self.current_weapon_name, {"ammo": 0, "magazines": 0})

        self.cached_ammo_texts = {}
        self.last_ammo_values = {}

    def loading_skin_player(self) -> list:
        self.skin_player = SettingsPlayer.skin_ust
        self.skin_player = find_in_json(data, "Skin", self.skin_player)
        return self.skin_player

    def change_skin_player(self) -> list:
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

    def load_default_weapon(self):
        inventory = SettingsLoot.InventoryCache
        if inventory:
            self.change_weapon(inventory[0])
        else:
            self.weapon_image = pygame.Surface((30, 30))
            self.weapon_image.fill((255, 0, 255))

    def change_weapon(self, item_name: str):
        self.path = find_in_json(data, GetKey.GetKeyObject, item_name)
        if self.path:
            try:
                raw = pygame.image.load(self.path)
                self.weapon_image = pygame.transform.scale(raw, (100, 60))
                self.current_weapon_name = item_name
                if item_name not in self.weapons_ammo:
                    self.weapons_ammo[item_name] = {"ammo": 30, "magazines": 2, "max_ammo": 30}
                self.current_weapon_stats = self.weapons_ammo[item_name]
            except Exception as e:
                print(f" {item_name}: {e}")
        else:
            print(f" {item_name} ")

    def has_ammo(self) -> bool:
        if self.current_weapon_name == "timeStopClock":
            return True
        return self.current_weapon_stats["ammo"] > 0

    def consume_ammo(self):
        if self.current_weapon_name != "timeStopClock" and self.current_weapon_stats["ammo"] > 0:
            self.current_weapon_stats["ammo"] -= 1

    def reload_weapon(self):
        if self.current_weapon_name == "timeStopClock":
            return
        if self.current_weapon_stats["magazines"] > 0 and self.current_weapon_stats["ammo"] < self.current_weapon_stats[
            "max_ammo"]:
            self.current_weapon_stats["magazines"] -= 1
            self.current_weapon_stats["ammo"] = self.current_weapon_stats["max_ammo"]

    def hot_slot_inventory(self, time_stop_cooldown_remaining=0):
        slot_width = HotSlotInventory.WidthHorInventorySlot
        slot_height = HotSlotInventory.HeightHotInventorySlot
        gap = HotSlotInventory.GapHotSlot
        start_x = HotSlotInventory.PosX
        start_y = HotSlotInventory.PosY
        count = HotSlotInventory.CountSlotHotSlot

        inventory = SettingsLoot.InventoryCache
        images = {}
        for i, item_name in enumerate(inventory[:count]):
            self.path = find_in_json("../settings.json", GetKey.GetKeyObject, item_name)
            if self.path:
                try:
                    img = pygame.image.load(self.path)
                    img = pygame.transform.scale(img, (slot_width, slot_height))
                    images[i] = img
                except:
                    images[i] = None

        for i in range(count):
            x = start_x + i * (slot_width + gap)
            y = start_y
            slot_rect = pygame.Rect(x, y, slot_width, slot_height)

            pygame.draw.rect(self.screen, HotSlotInventory.ColorHotSlot["Gray"], slot_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), slot_rect, 2)

            if i < len(inventory):
                img = images.get(i)
                item_name = inventory[i]
                if img:
                    self.screen.blit(img, slot_rect)

                    if item_name == "timeStopClock" and time_stop_cooldown_remaining > 0:
                        overlay = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)
                        center = (slot_width // 2, slot_height // 2)
                        radius = min(slot_width, slot_height) // 2 - 4
                        pygame.draw.circle(overlay, (0, 0, 0, 180), center, radius + 2)
                        progress = time_stop_cooldown_remaining / SettingsAmmo.TimeStopCooldown
                        start_angle = -math.pi / 2
                        end_angle = start_angle + (2 * math.pi * progress)
                        arc_rect = pygame.Rect(2, 2, slot_width - 4, slot_height - 4)
                        pygame.draw.arc(overlay, (0, 255, 255), arc_rect, start_angle, end_angle, 4)
                        self.screen.blit(overlay, (slot_rect.x, slot_rect.y))

                    if item_name in self.weapons_ammo:
                        stats = self.weapons_ammo[item_name]
                        if stats["ammo"] == float('inf'):
                            current_text = "∞"
                        else:
                            current_text = f"{stats['ammo']} | {stats['magazines']}"

                        if self.last_ammo_values.get(i) != current_text:
                            self.cached_ammo_texts[i] = self.ammo_font.render(current_text, True, (200, 200, 200))
                            self.last_ammo_values[i] = current_text

                        text_surf = self.cached_ammo_texts.get(i)
                        if text_surf:
                            text_x = slot_rect.x + slot_width // 2 - text_surf.get_width() // 2
                            text_y = slot_rect.y + slot_height - text_surf.get_height() - 2
                            self.screen.blit(text_surf, (text_x, text_y))

    def update(self, obstacles=None):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_d]:
            dx += self.speed

        self.is_moving = (keys[pygame.K_a] or keys[pygame.K_d] or
                          keys[pygame.K_w] or keys[pygame.K_s])

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
        return self.position

    def update_weapon_angle(self, mouse_pos):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        dx = mouse_pos[0] - cx
        dy = mouse_pos[1] - cy
        self.weapon_angle = math.degrees(math.atan2(-dy, dx))

    def draw_weapon(self, screen):
        offset_x = 20
        offset_y = 10
        rad = math.radians(self.weapon_angle)
        rot_offset_x = offset_x * math.cos(rad) - offset_y * math.sin(rad)
        rot_offset_y = offset_x * math.sin(rad) + offset_y * math.cos(rad)
        center_x = self.x + self.width / 2 + rot_offset_x
        center_y = self.y + self.height / 2 + rot_offset_y
        rotated = pygame.transform.rotate(self.weapon_image, self.weapon_angle)
        rect = rotated.get_rect(center=(center_x, center_y))
        screen.blit(rotated, rect)

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
        self.hot_slot_inventory()
        self.loading_skin_player()
        self.rect_player()
        self.display_health_point()

    def get_position(self) -> dict:
        self.update()
        print(self.position)
        return self.position
