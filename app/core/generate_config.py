import json

def generate_config(
        font_size: int,
        avatar_position: tuple,
        components: list,
        foundation,
        optional=None):
    base_config = open("templates/_template.json", "r")
    base_config = json.load(base_config)

    base_config["root_id"] = ""
    base_config["font"]["size"] = font_size
    base_config["avatar_position"] = avatar_position
    base_config["components"] += components

    print(base_config)

    