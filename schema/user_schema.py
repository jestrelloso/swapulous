from datetime import date, datetime
from enum import Enum
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, Field


# Enum class for gender
class genderChoices(str, Enum):
    male = "male"
    female = "female"
    other = "other"


# Enum class for user type
class userTypeChoices(str, Enum):
    Admin = "Admin"
    User = "User"
    Demo = "Demo"


# Base request model
class UserBase(BaseModel):
    username: str
    address: str
    bio: str
    changeProfile: bool = Field(default=False)
    city: str
    country: str
    dob: date
    emailConfirmed: bool = Field(default=False)
    firstLogin: bool = Field(default=True)
    firstName: str
    fullName: str
    gender: genderChoices
    isActive: bool = Field(default=True)
    lastName: str
    phoneNumber: str
    state: str
    street: str
    userType: userTypeChoices = Field(default=userTypeChoices.User.value)
    zipCode: str
    password: str
    email: str
    image: Optional[str] = None
    coverPhoto: Optional[str] = None


# Response model for User endpoints
class UserResponse(BaseModel):
    id: str
    username: str
    address: str
    bio: str
    changeProfile: bool
    city: str
    country: str
    dob: date
    emailConfirmed: bool
    firstLogin: bool
    firstName: str
    fullName: str
    gender: genderChoices
    isActive: bool
    lastName: str
    phoneNumber: str
    state: str
    street: str
    userType: userTypeChoices
    zipCode: str
    email: str
    createdDate: datetime
    image: Optional[str] = None
    coverPhoto: Optional[str] = None

    class Config:
        orm_mode = True


# Patch request model
class UserUpdatePatch(BaseModel):
    username: Optional[str]
    email: Optional[str]
    address: Optional[str]
    bio: Optional[str]
    changeProfile: Optional[bool]
    city: Optional[str]
    country: Optional[str]
    dob: Optional[date]
    emailConfirmed: Optional[bool]
    firstLogin: Optional[bool]
    firstName: Optional[str]
    fullName: Optional[str]
    gender: Optional[genderChoices]
    isActive: Optional[bool]
    lastName: Optional[str]
    phoneNumber: Optional[str]
    state: Optional[str]
    street: Optional[str]
    userType: Optional[userTypeChoices]
    zipCode: Optional[str]
    password: Optional[str]
    image: Optional[str]
    coverPhoto: Optional[str]
