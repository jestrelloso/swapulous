from fastapi import FastAPI
from model import models
from router import item_router
from router import user_router
from security import authentication
from db.database import Base, engine
from router import review
from model import models
from db.database import engine

# FastAPI instance
app = FastAPI()
app.include_router(item_router.router)

# Create database tables
models.Base.metadata.create_all(engine)

# Routers here
app.include_router(user_router.router)
app.include_router(authentication.router)
app.include_router(review.router)

# Testing
@app.get("/")
def index():
    return {'message': 'Hello World'}

models.Base.metadata.create_all(engine)