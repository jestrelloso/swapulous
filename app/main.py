from fastapi import FastAPI
from router import review
from model import models
from db.database import engine

app = FastAPI()

app.include_router(review.router)

@app.get('/')
def index():
    return {'message': 'Hello World'}

models.Base.metadata.create_all(engine)