from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import create_user, get_user_by_username, get_users
from app.schemas.user import UserCreate, User
from app.Config.database import get_db
from typing import List
from app.utils.hashing import pwd_context
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.auth import create_access_token, check_admin

router = APIRouter()

# creating user
@router.post("/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered.")
    db_user = create_user(db=db, user=user)
    return db_user


# login user endpoint
@router.post("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "Bearer"}


# reading a user by username
@router.get("/user/{username}", response_model=User)
async def read_user_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# reading all users
@router.get("/all", response_model=List[User], dependencies=[Depends(check_admin)])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=400, detail="No user registered yet.")
    return users
