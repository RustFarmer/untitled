import pygame
import json
from NoIdeaGamePygame.module import SettingsScreenPer, ObjectPath, SettingsLoot, find_in_json, GetKey

with open("../settings.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

class Inventory:
    def __init__(self):
        self.M416_scale = None
        self.M416 = None
        self.image_M416 = None
        self.count_loot: int = 0
        self.image_Ak = None
        self.Ak_scale = None
        self.Ak = None
        pygame.init()
        self._width = SettingsScreenPer.width
        self._height = SettingsScreenPer.height
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill(SettingsScreenPer.Black)
        self.event = None
        self.DONE = False
        self.size_mesh_inventory_Ak = SettingsLoot.Ak["sizeInInventory"]
        self.size_mesh_inventory_M416 = SettingsLoot.M416["sizeInInventory"]
        self.Invt_Cache = SettingsLoot.InventoryCache
        # print(self.Invt_Cache)

        self.color = data.get("ColorInventory", {}).get("Gray", [79, 79, 79])

        size_mesh = data.get("SettingsInventory", {}).get("size_mesh")
        if size_mesh is None:
            size_mesh = data.get("SettingsInventory", {}).get("size_mesh ", [150, 150])
        self.slot_size = size_mesh if size_mesh else [150, 150]

    def add_loot(self):
        self.image_Ak = str(ObjectPath.Ak)
        self.Ak = pygame.image.load(self.image_Ak)
        self.Ak_scale = pygame.transform.scale(self.Ak, self.size_mesh_inventory_Ak)

        self.image_M416 = ObjectPath.M416
        self.M416 = pygame.image.load(self.image_M416)
        self.M416_scale = pygame.transform.scale(self.M416, self.size_mesh_inventory_Ak)

    def draw_inventory(self):
        self.add_loot()

        images = {}
        for name in self.Invt_Cache:
            path = find_in_json(data, GetKey.GetKeyObject, name)
            if path:
                try:
                    img = pygame.image.load(path)
                    scaled = pygame.transform.scale(img, self.size_mesh_inventory_Ak)
                    images[name] = scaled
                except Exception as e:
                    print(f"Не удалось загрузить {path}: {e}")
                    images[name] = None
            else:
                images[name] = None

        rows, cols = 4, 4
        slot_width, slot_height = self.slot_size
        spacing = 10

        total_width = cols * slot_width + (cols - 1) * spacing
        total_height = rows * slot_height + (rows - 1) * spacing
        start_x = (self._width - total_width) // 2
        start_y = (self._height - total_height) // 2

        while not self.DONE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.DONE = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.DONE = True

            self.screen.fill(SettingsScreenPer.Black)

            for row in range(rows):
                for col in range(cols):
                    x = start_x + col * (slot_width + spacing)
                    y = start_y + row * (slot_height + spacing)
                    slot_rect = pygame.Rect(x, y, slot_width, slot_height)

                    pygame.draw.rect(self.screen, self.color, slot_rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), slot_rect, 2)

                    idx = row * cols + col
                    if idx < len(self.Invt_Cache):
                        item_name = self.Invt_Cache[idx]
                        surface = images.get(item_name)
                        if surface:
                            self._draw_item_in_slot(surface, slot_rect)


            pygame.display.update()

        self.screen.fill(SettingsScreenPer.Black)
        pygame.display.flip()

    def _draw_item_in_slot(self, image, slot_rect):
        """Центрирует изображение в слоте и рисует."""
        img_rect = image.get_rect(center=slot_rect.center)
        self.screen.blit(image, img_rect)
