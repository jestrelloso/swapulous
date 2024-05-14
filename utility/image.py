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


# Image handler function for coverPhoto field
async def save_more(moreimages: List[UploadFile], filenames: List[str]):
    try:
        os.makedirs("files/morephotos", exist_ok=True)
        for moreimage, filename in zip(moreimages, filenames):
            image_path = os.path.join("files/morephotos", filename)
            with open(image_path, "wb") as buffer:
                content = await moreimage.read()
                buffer.write(content)
            return image_path
    except Exception as e:
        print(f"Error saving images: {e}")
        return None
