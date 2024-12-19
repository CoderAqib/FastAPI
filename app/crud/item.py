from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

# display all items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate, user_id: int):
    db_item = Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# fetch/show item by title
def get_item_by_title(db: Session, title: str):
    return db.query(Item).filter(Item.title == str(title)).first()
