from sqlite3 import Date
import uuid
from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.types import Date

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
