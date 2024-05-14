
from sqlite3 import Date
import uuid
from uuid import uuid4
from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

# Table for User
class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, index=True, unique=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    address = Column(String)
    bio = Column(String)
    changeProfile = Column(Boolean)
    city = Column(String)
    country = Column(String)
    dob = Column(Date)
    emailConfirmed = Column(Boolean)
    firstLogin = Column(Boolean)
    firstName = Column(String, nullable=False)
    fullName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String)
    isActive = Column(Boolean)
    lastName = Column(String, nullable=False)
    phoneNumber = Column(String)
    state = Column(String)
    street = Column(String)
    userType = Column(String)
    modifiedDate = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    createdDate = Column(DateTime, default=func.now(), nullable=False)
    zipCode = Column(String)
    password = Column(String, nullable=False)
    image = Column(String, nullable=True)
    coverPhoto = Column(String, nullable=True)

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

class DbReview(Base):
    __tablename__= 'reviews'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    rating = Column(Integer)
    item = Column(String)
    comment =  Column(String)
    user = Column(String)
    creator = Column(String)
    modified_date = Column(String)
    created_date = Column(String)
    slug = Column(String)