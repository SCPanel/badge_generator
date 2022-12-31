import json
from os import mkdir, path

def generate_config(
        font_size: int,
        avatar_position: tuple,
        components: list,
        foundation,
        optional=None):
    base_config = open("templates/_template.json", "r")
    base_config = json.load(base_config)

    base_config["root_id"] = foundation["_id"]
    base_config["owner"] = foundation["owner"]
    base_config["font"]["size"] = font_size
    base_config["avatar_position"] = avatar_position
    base_config["components"] += components

    if optional:
        base_config["optional"] += optional

    
    if not path.exists(f"templates/{foundation['_id']}"):
        mkdir(f"templates/{foundation['_id']}")

    with open(f"templates/{foundation['_id']}/template_schema.json", "w") as config_file:
        json.dump(base_config, config_file, indent=4)

    return base_config
    