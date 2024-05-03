from fastapi import FastAPI
from model import models
from router import item_router, item_image_router
from router import user_router
from security import authentication
from db.database import Base, engine


# FastAPI instance
app = FastAPI()
app.include_router(item_router.router)
app.include_router(item_image_router.router)

# Create database tables
models.Base.metadata.create_all(engine)

# Routers here
app.include_router(user_router.router)
app.include_router(authentication.router)


# Testing
@app.get("/")
def index():
    return {"message": "Hello world!"}
