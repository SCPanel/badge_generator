from random import randint
from PIL import (
    Image,
    ImageDraw,
    ImageFont
)


class Generator:
    async def from_json(config, avatar=None):
        _project_root = f"templates/{config['root_id']}"

        if not avatar:
            avatar = f"{_project_root}/{config['avatar']}"

        _template = config["template"]


        if config.get("optional"):
            for _condition in config["optional"]:

                match _condition["condition"][0]: 
                    case "bool":
                        # Hardcode bool condition for template
                        if _condition[_condition["condition"][1]] and _condition["condition"][2] == "template":
                            _template = _condition["value"]

                    case _: 
                        raise


        img = Image.open(f"{_project_root}/{_template}")
        I1 = ImageDraw.Draw(img)

        
        def write_text(
            position,
            text,
            font_size=config["font"]["size"],
            stroke_width=0,
            color="black"):

            I1.text(
                position,
                text,
                font=ImageFont.truetype(f"{_project_root}/{config['font']['path']}", font_size),
                fill=color,
                stroke_fill=color,
                stroke_width=stroke_width)
        
        img.paste(
            Image.open(avatar),
            (config["avatar_position"]["x"],
            config["avatar_position"]["y"]),
        )

        for _component in config["components"]:
            match _component["type"]:
                case "text":
                    if _component.get("condition"):
                        for _condition in _component["condition"]:
                            match _condition[0]:
                                case "prefix":
                                    if not _component["value"].startswith(_condition[1]):
                                        raise
                                    
                                case "length":
                                    match _condition[1]:
                                        case "max":
                                            if len(_component["value"]) > _condition[2]:
                                                raise

                                        case "min":
                                            if len(_component["value"]) < _condition[2]:
                                                raise 

                                        case _:
                                            if len(_component["value"]) != _condition[2]:
                                                raise

                    write_text(
                        (
                            _component["position"]["x"],
                            _component["position"]["y"]
                        ),
                        _component["value"]
                    )
                case _:
                    raise

        # img.show()
        return img