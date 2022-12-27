from pydantic import BaseModel
from typing import Optional


class Position(BaseModel):
    x: int
    y: int


class Component(BaseModel):
    type: str
    value: str
    position: Position
    condition: Optional[list]