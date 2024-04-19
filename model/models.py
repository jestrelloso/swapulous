from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column, func, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from db.database import Base
import uuid


class DbItems(Base):
    __tablename__ = 'items'
    id = Column(String, primary_key=True, index = True, unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    appversion = Column(String)
    availability = Column(String)
    city = Column(String)
    condition = Column(String)
    description = Column(String)
    isfree = Column(Boolean)
    oscategory = Column(String)
    ossubcategory = Column(String)
    price = Column(Integer)
    shortinfo = Column(String)
    state = Column(String)
    status = Column(String)
    version = Column(String)
    reviews = Column(String)
    modifieddate = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    createddate = Column(DateTime, default=func.now(), nullable=False)
    mainimage = Column(String, nullable=True)
    moreimage = relationship("ItemsImage", back_populates='item', cascade="all, delete-orphan")
    
class ItemsImage(Base):
    __tablename__ = 'images'
    id = Column(String, primary_key=True, index = True, unique=True, default=lambda: str(uuid.uuid4()))
    image_path = Column(String, nullable=False)
    item_id = Column(String, ForeignKey("items.id", ondelete="CASCADE"))
    item = relationship("DbItems", back_populates='moreimage')
