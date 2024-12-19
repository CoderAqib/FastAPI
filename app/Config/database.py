from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_url = "sqlite:///./my_db.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False, "timeout": 30})
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()