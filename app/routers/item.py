from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.item import get_items, create_item, get_item_by_title
from app.crud.user import get_user_by_id
from app.schemas.item import ItemCreate, Item
from app.Config.database import get_db
from typing import List

router = APIRouter()


# Calling item create function from crud
@router.post("/Users/{user_id}", response_model=Item)
async def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="this user is not registered")
    return create_item(db=db, item=item, user_id=user_id)


# reading all items
@router.get("/all", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    if not items:
        raise HTTPException(status_code=400, detail="No item found.")
    return items


# reading an item by title
@router.get("/{title}", response_model=Item)
async def read_item_by_title(title: str, db: Session = Depends(get_db)):
    item = get_item_by_title(db=db, title=title)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
