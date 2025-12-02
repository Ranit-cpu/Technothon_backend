from fastapi import APIRouter
import os

router = APIRouter()

GALLERY_DIR = "uploads/gallery"
BACKEND_URL = "http://localhost:8000"  # Or use environment variable

@router.get("/gallery")
def get_gallery_images():
    files = []
    if os.path.exists(GALLERY_DIR):
        for idx, filename in enumerate(os.listdir(GALLERY_DIR), start=1):
            files.append({
                "id": idx,
                "image": f"{BACKEND_URL}/uploads/gallery/{filename}"
            })
    return {"gallery": files}