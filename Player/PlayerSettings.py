import json
import pygame
from NoIdeaGamePygame.module import SettingsPlayer, find_in_json, update_json_value
from NoIdeaGamePygame.Player.Sraw_inventory import Inventory

def save_position(position):
    data = "../settings.json"
    update_json_value(data, "Player.position", position)


class Player:
    def __init__(self, screen):
        self.position = None
        self.screen = screen
        self.event = None
        self.start_health = None
        self.health = None
        self.skin_player = None
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
        with open("../settings.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(data)
            print(self.skin_player)
        self.skin_player = find_in_json(data, "Skin", self.skin_player)
        return self.skin_player

    def change_health_point(self, damage: int) -> int:
        self.start_health = SettingsPlayer.Health
        self.health = self.start_health - damage
        return self.health

    def change_position(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.y -= self.scale_move
            elif event.key == pygame.K_s:
                self.y += self.scale_move
            elif event.key == pygame.K_a:
                self.x -= self.scale_move
            elif event.key == pygame.K_d:
                self.x += self.scale_move
            elif event.key == pygame.K_ESCAPE:
                print('uit0vbw89487t')

    def update(self):
        keys = pygame.key.get_pressed()
        self.position = [self.x, self.y]
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_TAB]:
            Inventory().draw_inventory()
        return self.position

    def display_health_point(self):

        pygame.draw.rect(self.screen, SettingsPlayer.ColorHealthPoint,
                         pygame.Rect(self.PositionHealthPoint_X, self.PositionHealthPoint_Y,
                                     self.PositionHealthPoint_width, self.PositionHealthPoint_height))

    def rect_player(self):
        pygame.draw.rect(self.screen, self.skin_player,
                         (self.x, self.y, self.width, self.height))

    def redy_player(self):
        self.loading_skin_player()
        self.rect_player()
        self.display_health_point()
