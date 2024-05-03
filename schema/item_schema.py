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

class ImageBase(BaseModel):
    image: Optional[str] = None
    item_id: str

class Item(BaseModel):
    item_id: str
    item_name: str
    class Config():
        orm_mode = True

class ImageDisplay(BaseModel):
    id: str
    item_id: str
    image: Optional[str] = None
    item: Item
    class Config():
        orm_mode = True

class MoreImage(BaseModel):
    image: str
    class Config():
        orm_mode = True
    
class ItemBase(BaseModel):
    name: str
    appversion: str
    availability: bool
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
    moreimage: List[MoreImage] = []
    class Config():
        orm_mode = True


class ItemResponse(BaseModel):
    id: str
    name: str
    appversion: str
    availability: bool
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
    class Config():
        orm_mode = True


class ItemUpdate(BaseModel):
    reviews: Optional[str]
    name: Optional[str]
    appversion: Optional[str]
    availability: Optional[bool]
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
    class Config():
        orm_mode = True