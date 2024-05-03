from fastapi import FastAPI
from router import item_router, item_image_router
from model import models
from db.database import engine


app = FastAPI()
app.include_router(item_router.router)
app.include_router(item_image_router.router)


models.Base.metadata.create_all(engine)

@app.get("/")
def index():
    return {"message": "Hello world!"}
