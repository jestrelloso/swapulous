import email
import os
from typing import Optional
import uuid
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    UploadFile,
    status,
    File,
    UploadFile,
)
from pydantic import ValidationError
from sqlalchemy import Null
from db.database import get_db
from schema.user_schema import UserBase, UserResponse, UserUpdatePatch
from model import models
from sqlalchemy.orm import Session
from security.hash import Hash

from utility.image_handler import save_cover, save_image

# Router instance
router = APIRouter(prefix="/user", tags=["User"])


# Create a user
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    request: str = Body(...),
    image_upload: Optional[UploadFile] = File(None),
    cover_upload: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Error handling if request body is invalid
    try:
        new_user = UserBase.parse_raw(request)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid request body.")

    # Check for missing fields which are inside the list
    if not all(
        getattr(new_user, field)
        for field in [
            "fullName",
            "firstName",
            "lastName",
            "email",
            "password",
            "username",
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail="Fields: fullName, firstName, lastName, username are required.",
        )

    # Check email if it already exists
    email_check = (
        db.query(models.User).filter(models.User.email == new_user.email).first()
    )
    if email_check:
        raise HTTPException(status_code=400, detail="Email already exists.")

    username_check = (
        db.query(models.User).filter(models.User.username == new_user.username).first()
    )
    if username_check:
        raise HTTPException(status_code=400, detail="Username already exists.")
    # Image handling
    if image_upload is not None:
        if not (
            image_upload.filename.endswith(".jpg")
            or image_upload.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Image must be of type .jpg or .png."
            )

        image_name = f"{new_user.username}_{str(uuid.uuid4())}.{image_upload.filename.split('.')[-1]}"
        user_image = await save_image(image_upload, image_name)
    else:
        user_image = None

    if cover_upload is not None:
        if not (
            cover_upload.filename.endswith(".jpg")
            or cover_upload.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Cover photo must be of type .jpg or .png."
            )
        cover_name = f"{new_user.username}_{str(uuid.uuid4())}.{cover_upload.filename.split('.')[-1]}"
        cover_photo = await save_cover(cover_upload, cover_name)
    else:
        cover_photo = None

    # Hashing the password and inserting the parsed JSON data into the database.
    hash_pass = Hash.bcrypt(new_user.password)
    new_user.password = hash_pass
    user_data = new_user.dict()
    user_data.pop("image", None)
    user_data.pop("coverPhoto", None)
    user = models.User(**user_data, image=user_image, coverPhoto=cover_photo)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# GET method for retrieving a specific user
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
    id: str,
    db: Session = Depends(get_db),
):
    # Db query to retrieve user
    fetch_user = db.query(models.User).filter(models.User.id == id).first()
    if not fetch_user:
        raise HTTPException(status_code=404, detail=f"User with {id} not found.")
    return fetch_user


# Delete a specific user. make sure to indicate what type of HTTP Request since it has the same URL as GET method
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: str, db: Session = Depends(get_db)):
    # Db query to fetch user
    fetch_user = db.query(models.User).filter(models.User.id == id).first()
    if not fetch_user:
        raise HTTPException(status_code=404, detail=f"User with {id} not found.")
    # Define folder paths based on user's username
    image_folder_path = os.path.join("files", "image")
    cover_photo_folder_path = os.path.join("files", "coverphoto")

    try:
        # Delete specific files in the image folder
        for filename in os.listdir(image_folder_path):
            if filename.startswith(fetch_user.username):
                file_path = os.path.join(image_folder_path, filename)
                os.remove(file_path)

        # Delete specific files in the cover photo folder
        for filename in os.listdir(cover_photo_folder_path):
            if filename.startswith(fetch_user.username):
                file_path = os.path.join(cover_photo_folder_path, filename)
                os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user files: {str(e)}"
        )
    # Delete the user
    db.delete(fetch_user)
    db.commit()
    return {"message": f"User with id: {id} is deleted."}


# Patch method for partially updating a specific user
@router.patch(
    "/{id}/update", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def patch_user(
    id: str,
    request: Optional[str] = Body(None),
    image_upload: UploadFile = File(None),
    cover_upload: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Query to retrieve user.
    fetch_user = db.query(models.User).filter(models.User.id == id).first()
    if not fetch_user:
        raise HTTPException(status_code=404, detail=f"User with {id} not found.")

    # Parse the request body into a dictionary
    if request is not None:
        try:
            request = UserUpdatePatch.parse_raw(request)
            request_dict = request.dict(exclude_unset=True)
            if "password" in request_dict:
                hash_pass = Hash.bcrypt(request_dict["password"])
                request_dict["password"] = hash_pass
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid request body.")

        # Check for empty string values for required fields
        required_fields = ["fullName", "firstName", "lastName", "email", "password", "username"]
        for field in required_fields:
            if field in request_dict and not request_dict[field]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' cannot be empty.",
                )

        # Retain existing data if fields are not present in request
        for field in required_fields:
            if field not in request_dict:
                request_dict[field] = getattr(fetch_user, field)

        check_email = (
            db.query(models.User).filter(models.User.email == request.email).first()
        )
        if check_email and check_email.id != id:
            raise HTTPException(status_code=400, detail="Email already exists.")
        username_check = (
            db.query(models.User)
            .filter(models.User.username == request.username)
            .first()
        )
        if username_check and username_check.id != id:
            raise HTTPException(status_code=400, detail="Username already exists.")
    else:
        request_dict = {}

    # Update only the fields present in the request
    for field, value in request_dict.items():
        setattr(fetch_user, field, value)

    # Handle image uploads
    if image_upload is not None:
        if not (
            image_upload.filename.endswith(".jpg")
            or image_upload.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Image must be of type .jpg or .png."
            )
        image_name = f"{fetch_user.username}_{str(uuid.uuid4())}.{image_upload.filename.split('.')[-1]}"
        user_image = await save_image(image_upload, image_name)
        fetch_user.image = user_image

    # Handle cover photo uploads
    if cover_upload is not None:
        if not (
            cover_upload.filename.endswith(".jpg")
            or cover_upload.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Cover photo must be of type .jpg or .png."
            )
        cover_name = f"{fetch_user.username}_{str(uuid.uuid4())}.{cover_upload.filename.split('.')[-1]}"
        cover_photo = await save_cover(cover_upload, cover_name)
        fetch_user.coverPhoto = cover_photo

    db.commit()
    db.refresh(fetch_user)
    return fetch_user


# PUT method for updating all fields for a specific user
@router.put(
    "/{id}/updateall", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def put_user(
    id: str,
    request: str = Body(...),
    image_upload: UploadFile = File(None),
    cover_upload: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Query to retrieve user.
    fetch_user = db.query(models.User).filter(models.User.id == id).first()
    if not fetch_user:
        raise HTTPException(status_code=404, detail=f"User with {id} not found.")

    # Parse the request body into a dictionary
    if request is not None:
        try:
            request = UserBase.parse_raw(request)
            request_dict = request.dict(exclude_unset=True)
            if request.password:
                hash_pass = Hash.bcrypt(request.password)
                request_dict["password"] = hash_pass
            if not all(
                getattr(request, field)
                for field in ["fullName", "firstName", "lastName", "email", "password", "username"]
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Fields: fullName, firstName, lastName, email, username, password are required.",
                )
            check_email = (
                db.query(models.User).filter(models.User.email == request.email).first()
            )
            if check_email:
                raise HTTPException(status_code=400, detail="Email already exists.")
            username_check = (
                db.query(models.User)
                .filter(models.User.username == request.username)
                .first()
            )
            if username_check:
                raise HTTPException(status_code=400, detail="Username already exists.")
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid request body.")

        if image_upload is not None:
            if not (
                image_upload.filename.endswith(".jpg")
                or image_upload.filename.endswith(".png")
            ):
                raise HTTPException(
                    status_code=400, detail="Image must be of type .jpg or .png."
                )
            image_name = f"{fetch_user.username}_{str(uuid.uuid4())}.{image_upload.filename.split('.')[-1]}"
            user_image = await save_image(image_upload, image_name)
            request_dict["image"] = user_image
        else:
            user_image = None

        if cover_upload is not None:
            if not (
                cover_upload.filename.endswith(".jpg")
                or cover_upload.filename.endswith(".png")
            ):
                raise HTTPException(
                    status_code=400, detail="Cover photo must be of type .jpg or .png."
                )
            cover_name = f"{fetch_user.username}_{str(uuid.uuid4())}.{cover_upload.filename.split('.')[-1]}"
            cover_photo = await save_cover(cover_upload)
            request_dict["coverPhoto"] = cover_photo
        else:
            cover_photo = None

        for field, value in request_dict.items():
            setattr(fetch_user, field, value)

        db.commit()
        db.refresh(fetch_user)
        return fetch_user
    else:
        raise HTTPException(status_code=400, detail="No request stated.")
