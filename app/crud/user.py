from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.hashing import get_hashed_password


# creating user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = User(username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# fetch/show user by id
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).options(joinedload(User.items)).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# fetch/showing all users
def get_users(db: Session, skip: int = 0, limit=100):
    return db.query(User).offset(skip).limit(limit).all()
