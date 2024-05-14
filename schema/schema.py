from pydantic import BaseModel
from datetime import date


class reviewBase(BaseModel):
    rating: int
    item: str
    comment: str
    user: str
    creator: str
    modified_date: date
    created_date: date
    slug: str
    class Config():
        orm_mode=True