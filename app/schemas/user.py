# Nested models in FastAPI allow including one Pydantic model as a field inside another model,
# enabling complex data structures with hierarchical relationships.

from pydantic import BaseModel
from typing import List
from enum import Enum
from app.schemas.item import Item

# Roles schema
class Roles(str, Enum):
    admin = "admin"
    user = "user"

# user schema
class UserBase(BaseModel):
    username: str
    role: Roles = "user"
   

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attributes = True