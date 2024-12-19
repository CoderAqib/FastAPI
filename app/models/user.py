from sqlalchemy import Column, Boolean, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.Config.database import base
from app.schemas.user import Roles

# User Model
class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Roles), default="user")
    items = relationship("Item", back_populates="owner")