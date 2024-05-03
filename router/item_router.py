from pydantic import ValidationError
from typing import Optional, List
import os
import uuid
import json
from sqlalchemy.orm.session import Session
from db.database import get_db
from model import models
from fastapi import APIRouter, Body, Depends, HTTPException, status, UploadFile, File
from schema.item_schema import ItemBase, ItemUpdate, ItemResponse
from utility.image import save_itemimage, save_more

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/createitem/", response_model=ItemResponse)
async def create_item(
    request: str = Body(...),
    main_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    try:
        new_item = ItemBase.parse_raw(request)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid request body.")

    if main_image is not None:
        if not (
            main_image.filename.endswith(".jpg") or main_image.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Image must be of type .jpg or .png."
            )

        image_name = (
            f"{new_item.name}_{str(uuid.uuid4())}.{main_image.filename.split('.')[-1]}"
        )
        item_image = await save_itemimage(main_image, image_name)
    else:
        item_image = None

    item_data = new_item.dict()
    item_data.pop("mainimage", None)
    item = models.DbItems(**item_data, mainimage=item_image)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# GET method for the retrieval of items
@router.get("/itemsgetall/")
def read_items(db: Session = Depends(get_db)):
    return db.query(models.DbItems).all()


# GET method for retrieving a specific item
@router.get("/{item_id}/itemget", response_model=ItemBase)
def read_item(id: str, db: Session = Depends(get_db)):
    item = db.query(models.DbItems).filter(models.DbItems.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no such item as {id}",
        )
    return item


from fastapi import HTTPException


# Define the endpoint for updating an item using PUT method
@router.put("/{item_id}/updateall", response_model=ItemResponse)
async def update_item(
    id: str,
    request: Optional[str] = Body(None),
    main_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    item = db.query(models.DbItems).filter(models.DbItems.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with name {id} not found",
        )
        
    if request is not None:
        try:
            request = ItemUpdate.parse_raw(request)
            request_dict = request.dict(exclude_unset=True)
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid request body.")
        
        required_fields = ["name", "city", "oscategory", "state", "status"]
        for field in required_fields:
            if field in request_dict and not request_dict[field]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' cannot be empty.",
                )
    else:
        request_dict = {}

    if main_image is not None:
        if not (
            main_image.filename.endswith(".jpg") or main_image.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Image must be of type .jpg or .png."
            )

        image_name = (
            f"{item.name}_{str(uuid.uuid4())}.{main_image.filename.split('.')[-1]}"
        )
        item_image = await save_itemimage(main_image, image_name)
        item.mainimage = item_image

    db.commit()
    db.refresh(item)
    return item


@router.patch("/{id}/itemchange", response_model=ItemUpdate)
async def partial_update_item(
    id: str,
    request: Optional[str] = Body(None),
    main_image: Optional[UploadFile] = File(None),
    # more_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    item = db.query(models.DbItems).filter(models.DbItems.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with name {id} not found",
        )
        
    if request is not None:
        try:
            request = ItemUpdate.parse_raw(request)
            request_dict = request.dict(exclude_unset=True)
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid request body.")
    else:
        request_dict = {}

    for field, value in request_dict.items():
        setattr(item, field, value)

    if main_image is not None:
        if not (
            main_image.filename.endswith(".jpg") or main_image.filename.endswith(".png")
        ):
            raise HTTPException(
                status_code=400, detail="Image must be of type .jpg or .png."
            )

        image_name = (
            f"{item.name}_{str(uuid.uuid4())}.{main_image.filename.split('.')[-1]}"
        )
        item_image = await save_itemimage(main_image, image_name)
        item.mainimage = item_image

    db.commit()
    db.refresh(item)
    return item


# Delete a specific item or an image/s from the item
@router.delete("/{item_id}/itemdelete")
def delete_user(id: str, db: Session = Depends(get_db)):
    item = db.query(models.DbItems).filter(models.DbItems.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"User with {id} not found.")
    image_folder_path = os.path.join("files", "itemimage")
    more_photo_folder_path = os.path.join("files", "morephotos")

    try:
        # Delete specific files in the image folder
        for filename in os.listdir(image_folder_path):
            if filename.startswith(item.id):
                file_path = os.path.join(image_folder_path, filename)
                os.remove(file_path)

        # Delete specific files in the more photo folder
        for filename in os.listdir(more_photo_folder_path):
            if filename.startswith(item.name):
                file_path = os.path.join(more_photo_folder_path, filename)
                os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete user files: {str(e)}"
        )
    db.delete(item)
    db.commit()
    return "Deleted the Item"
