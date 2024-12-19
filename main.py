from fastapi import FastAPI
from app.routers import user, item
from app.Config.database import base, engine

base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(item.router, prefix="/items", tags=["Items"])
