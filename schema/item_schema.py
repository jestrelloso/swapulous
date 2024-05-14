from sqlalchemy import Column, func, DateTime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class conds(str, Enum):
    Damaged = "Damaged"
    Refurbished = "Refurbished"
    Unused = "Unused"

class Category(str, Enum):
    Electronic = "Electronic"
    Media = "Media"


class ItemBase(BaseModel):
    name: str
    appversion: str
    availability: str
    city: str
    condition: conds 
    description: str
    isfree: bool
    oscategory: str
    ossubcategory: str
    price: float
    shortinfo: str
    state: str
    status: str
    version: str
    reviews: str
    mainimage: Optional[str] = None
    moreimage: Optional[str] = None
    class Config():
        orm_mode = True


class ItemResponse(BaseModel):
    id: str
    name: str
    appversion: str
    availability: str
    city: str
    condition: conds 
    description: str
    isfree: bool
    oscategory: str
    ossubcategory: str
    price: float
    shortinfo: str
    state: str
    status: str
    version: str
    reviews: str
    mainimage: Optional[str] = None
    moreimage: Optional[str] = None
    class Config():
        orm_mode = True

class ItemUpdate(BaseModel):
    reviews: Optional[str]
    name: Optional[str]
    appversion: Optional[str]
    availability: Optional[str]
    city: Optional[str]
    condition: Optional[conds] 
    description: Optional[str]
    isfree: Optional[bool]
    oscategory: Optional[str]
    ossubcategory: Optional[str]
    price: Optional[float]
    shortinfo: Optional[str]
    state: Optional[str]
    status: Optional[str]
    version: Optional[str]
    mainimage: Optional[str]
    moreimage: Optional[str]
    class Config():
        orm_mode = True