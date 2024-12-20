from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.Config.database import base

# Item model
class Item(base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="items")