import os
from fastapi import UploadFile


# Image handler function for image field
async def save_image(image: UploadFile, filename: str):
    try:
        os.makedirs("files\image", exist_ok=True)
        image_path = os.path.join("files\image", filename)
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        return image_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None


# Image handler function for coverPhoto field
async def save_cover(cover_image: UploadFile, filename: str):
    try:
        os.makedirs("files\coverphoto", exist_ok=True)
        image_path = os.path.join("files\coverphoto", filename)
        with open(image_path, "wb") as buffer:
            content = await cover_image.read()
            buffer.write(content)
        return image_path
    except Exception as e:
        print(f"Error saving cover image: {e}")
        return None
