import json


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
                raise KeyError(f"Ключ '{key}'")
        current = current[key]

    last_key = keys[-1]

    if not create_missing and last_key not in current:
        raise KeyError(f"Ключ '{last_key}' в {keys}")

    current[last_key] = new_value

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
