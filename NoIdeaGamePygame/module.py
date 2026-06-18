import json

data = "../settings.json"


def find_in_json(data_path, GetKey, target_find) -> list or None:
    try:
        with open(data_path, 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
    except FileNotFoundError:
        print("FILE NOT FOUND SETTINGS.JSON")

    colors_dict = data.get(str(GetKey))
    if colors_dict and target_find in colors_dict:
        return colors_dict[target_find]
    else:
        return None


def update_json_value(file_path, key_path, new_value, create_missing=False):

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(data["Player"]['position'], '-MODULE-0', new_value)

    if isinstance(key_path, str):
        keys = key_path.split('.')
    else:
        keys = key_path

    current = data
    for key in keys[:-1]:
        if key not in current:
            if create_missing:
                current[key] = {}
            else:
                raise KeyError(f"Ключ '{key}' не найден. Используйте create_missing=True, чтобы создать его.")
        current = current[key]

    last_key = keys[-1]
    print(current[last_key], '|', new_value)

    if not create_missing and last_key not in current:
        raise KeyError(f"Ключ '{last_key}' не найден в {keys}")

    current[last_key] = new_value
    print(current[last_key], '|2|', new_value)

    with open(file_path, 'w', encoding='utf-8') as f:
        print(data["Player"]['position'], "|3|")
        json.dump(data, f, indent=4, ensure_ascii=False)


class GetKey:
    GetKeySettingsScreenColor: str = "Color"
    GetKeyObjectScreenParameter: str = "ParameterScreen"
    GeKeyObjectPlayer: str = "Player"
    GetKeyObject: str = "Path_In_Object_Model"
    GetKeyInventory: str = "SettingsInventory"
    SettingsLoot: str = "SpecificationsLoot"
    SettingsWeapon: str = "SettingsWeapon"


class SettingsScreenPer:
    Black: list
    White: list
    Brown: list
    width: int
    height: int
    FirstSetting_x: int
    FirstSetting_y: int

    Black = find_in_json(data, GetKey.GetKeySettingsScreenColor, "Black")
    White = find_in_json(data, GetKey.GetKeySettingsScreenColor, "White")
    Brown = find_in_json(data, GetKey.GetKeySettingsScreenColor, "Brown")

    width = find_in_json(data, GetKey.GetKeyObjectScreenParameter, "width")
    height = find_in_json(data, GetKey.GetKeyObjectScreenParameter, "height")

    FirstSetting_dict = find_in_json(data, "SettingLayerGame", "first")
    if FirstSetting_dict:
        FirstSetting_x = FirstSetting_dict.get("x", 0)
        FirstSetting_y = FirstSetting_dict.get("y", 0)
    else:
        FirstSetting_x = 0
        FirstSetting_y = 0


class SettingsPlayer:
    Name: str
    Skin: dict

    Health: int
    ColorHealthPoint: int
    PositionHealthPoint: int
    PositionHealthPoint_width_height: int

    Level: int
    Score: int

    PositionX: int
    PositionY: int

    Width_player: int
    Height_player: int

    Speed: int
    Scale_move: int

    Inventory: list

    Name = find_in_json(data, GetKey.GeKeyObjectPlayer, "name")

    Skin = find_in_json(data, GetKey.GeKeyObjectPlayer, "skin")
    skin_ust = find_in_json(data, GetKey.GeKeyObjectPlayer, "skin_ust")

    Health = find_in_json(data, GetKey.GeKeyObjectPlayer, "health")
    ColorHealthPoint = find_in_json(data, GetKey.GeKeyObjectPlayer, "ColorHealthPoint")
    PositionHealthPoint = find_in_json(data, GetKey.GeKeyObjectPlayer, "PositionHealthPoint")
    PositionHealthPoint_width_height = find_in_json(data, GetKey.GeKeyObjectPlayer, "Width_Height_HealthPoint")

    Level = find_in_json(data, GetKey.GeKeyObjectPlayer, "level")
    Score = find_in_json(data, GetKey.GeKeyObjectPlayer, "score")

    Width_player = find_in_json(data, GetKey.GeKeyObjectPlayer, "width_player")
    Height_player = find_in_json(data, GetKey.GeKeyObjectPlayer, "height_player")

    Inventory = find_in_json(data, GetKey.GeKeyObjectPlayer, "inventory")

    Position = find_in_json(data, GetKey.GeKeyObjectPlayer, "position")

    PositionX, PositionY = Position[0], Position[1]

    Speed = find_in_json(data, GetKey.GeKeyObjectPlayer, "speed")
    Scale_move = find_in_json(data, GetKey.GeKeyObjectPlayer, "scale_move")


class ControlsPlayer:
    ControlsPlayer: dict

    ControlsPlayer = find_in_json(data, GetKey.GeKeyObjectPlayer, "ControlsPlayer")


class Inventory:
    WidthInventorySlot: int
    HeightInventorySlot: int

    WidthInventorySlot = find_in_json(data, GetKey.GetKeyInventory, "size_mesh")


class ObjectPath:
    Ak: str

    Ak = find_in_json(data, GetKey.GetKeyObject, "ak")
    M416 = find_in_json(data, GetKey.GetKeyObject, "m416")


class SettingsLoot:
    Ak: str
    TimeSpawn: int = 1

    InventoryCache: str

    InventoryCache = find_in_json(data, GetKey.GeKeyObjectPlayer, "inventory")
    Ak = find_in_json(data, GetKey.SettingsLoot, "ak")
    M416 = find_in_json(data, GetKey.SettingsLoot, "m416")


class SettingsWeapon:
    with_Ak: str
    height_ak: str
    ColorBullet: int
    BulletSpeed: int

    with_height_color_ak = find_in_json(data, GetKey.SettingsWeapon, "ak")
    with_Ak = with_height_color_ak["with_Ak"]
    height_ak = with_height_color_ak["heightAk"]
    ColorBullet = with_height_color_ak["colorBulletAk"]
    BulletSpeed = with_height_color_ak.get("bullet_speed", 5)
    FireRate = with_height_color_ak.get("fire_rate", 200)