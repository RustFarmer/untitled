import json


def find_in_json(data, GetKey, target_find) -> list or None:
    colors_dict = data.get(str(GetKey))
    if colors_dict and target_find in colors_dict:
        return colors_dict[target_find]
    else:
        return None


def update_json_value(file_path, key_path, new_value, create_missing=False):

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

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
    if not create_missing and last_key not in current:
        raise KeyError(f"Ключ '{last_key}' не найден в {keys}")

    current[last_key] = new_value

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


with open("../settings.json", 'r', encoding='utf-8') as file:
    data = json.load(file)


class GetKey:
    GetKeySettingsScreenColor: str = "Color"
    GetKeyObjectScreenParameter: str = "ParameterScreen"
    GeKeyObjectPlayer: str = "Player"
    GetKeyObject: str = "Path_In_Object_Model"
    GetKeyInventory: str = "SettingsInventory"
    SettingsLoot: str = "SpecificationsLoot"


class SettingsScreenPer:
    Black: list
    White: list
    Brown: list

    width: int
    height: int
    data: dict

    FirstSetting_x: int
    FirstSetting_y: int
    try:
        with open("../settings.json", 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
    except FileNotFoundError:
        print("FILE NOT FOUND SETTINGS.JSON")

    Black: list = find_in_json(data, GetKey.GetKeySettingsScreenColor, "Black")
    White: list = find_in_json(data, GetKey.GetKeySettingsScreenColor, "White")
    Brown: list = find_in_json(data, GetKey.GetKeySettingsScreenColor, "Brown")

    width: int = find_in_json(data, GetKey.GetKeyObjectScreenParameter, "width")
    height: int = find_in_json(data, GetKey.GetKeyObjectScreenParameter, "height")

    FirstSetting: int = find_in_json(data, "SettingLayerGame", "first")
    FirstSetting_x, FirstSetting_y = FirstSetting["x"], FirstSetting["y"]


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

    with open("../settings.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

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

    Speed = find_in_json(data, GetKey.GeKeyObjectPlayer, "speed")
    Scale_move = find_in_json(data, GetKey.GeKeyObjectPlayer, "scale_move")

    if Position:
        PositionX, PositionY = Position[0], Position[1]
    else:
        PositionX, PositionY = 0, 0


class ControlsPlayer:
    ControlsPlayer: dict

    with open("../settings.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    ControlsPlayer = find_in_json(data, GetKey.GeKeyObjectPlayer, "ControlsPlayer")


class Inventory:
    WidthInventorySlot: int
    HeightInventorySlot: int

    with open("../settings.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    WidthInventorySlot = find_in_json(data, GetKey.GetKeyInventory, "size_mesh")


class ObjectPath:
    Ak: str

    with open("../settings.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    Ak = find_in_json(data, GetKey.GetKeyObject, "ak")
    M416 = find_in_json(data, GetKey.GetKeyObject, "m416")


class SettingsLoot:
    Ak: str
    TimeSpawn: int = 1

    InventoryCache: str

    InventoryCache = find_in_json(data, GetKey.GeKeyObjectPlayer, "inventory")
    Ak = find_in_json(data, GetKey.SettingsLoot, "ak")
    M416 = find_in_json(data, GetKey.SettingsLoot, "m416")
