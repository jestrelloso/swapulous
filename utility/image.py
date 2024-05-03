import os
from typing import List
from fastapi import UploadFile


# Image handler function for image field
async def save_itemimage(image: UploadFile, filename: str):
    try:
        os.makedirs("files\itemimage", exist_ok=True)
        image_path = os.path.join("files\itemimage", filename)
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        return image_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


# Image handler function for additionalImage field
async def save_more(moreimages: UploadFile, filename: str):
    try:
        os.makedirs("files\morephotos", exist_ok=True)
        image_path = os.path.join("files\morephotos", filename)
        with open(image_path, "wb") as buffer:
            content = await moreimages.read()
            buffer.write(content)
        return image_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
