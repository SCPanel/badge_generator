from pydantic import (
    BaseModel,
    conlist
)
from typing import Optional, List
from app.core.models.general import Position, Component

class FoundationSchema(BaseModel):
    font_size: int
    avatar_position: Position
    components: conlist(Component, min_items=1) 
    optional: Optional[list]



