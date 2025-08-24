from fastapi import APIRouter
import os

router = APIRouter()

GALLERY_DIR = "uploads/gallery"

@router.get("/gallery")
def get_gallery_images():
    files = []
    if os.path.exists(GALLERY_DIR):
        for idx, filename in enumerate(os.listdir(GALLERY_DIR), start=1):
            files.append({
                "id": idx,
                "image": f"/uploads/gallery/{filename}"
            })
    return {"gallery": files}