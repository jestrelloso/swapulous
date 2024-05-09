from pydantic import ValidationError
from typing import Optional, List, Any
import os
import uuid
import json
import shutil
from sqlalchemy.orm.session import Session
from db.database import get_db, SessionLocal
from model import models
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from schema.item_schema import ImageBase, ImageDisplay
from utility.image import save_more


router = APIRouter(prefix="/image", tags=["image"])



from fastapi import HTTPException

@router.post("/upload_image/")
async def upload_image(item_id: str, moreimages: UploadFile = File(...)):
    # Save the image with its respective item_id string to the filesystem
    image_name = (
            f"{item_id}_{str(uuid.uuid4())}.{moreimages.filename.split('.')[-1]}"
        )
    image_path = await save_more(moreimages, image_name)
    
    if image_path:
        # Create a DB ImageBase object to store in the database
        image_data = models.ItemsImage(item_id=item_id, image=image_path)
        
        # Add image_data to the database session and commit changes
        db = SessionLocal()
        try:
            db.add(image_data)
            db.commit()
            db.refresh(image_data)
            return {"id": image_data.id, "item_id": image_data.item_id, "image": image_data.image}
        finally:
            db.close()
    else:
        return {"error": "Failed to save image"}

