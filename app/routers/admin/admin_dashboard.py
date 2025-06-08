from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.admin_models import Admin
from app.models.participant_models import Participant
from app.database import get_session

router = APIRouter()

@router.get("/admin")
async def admin_dashboard(request: Request, db: AsyncSession = Depends(get_session)):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Validate that the admin exists
    result = await db.execute(select(Admin).where(Admin.admin_id == admin_id))
    admin = result.scalar_one_or_none()
    if not admin:
        raise HTTPException(status_code=403, detail="Admin not found")

    # Fetch all participants
    result = await db.execute(select(Participant))
    participants = result.scalars().all()

    # Exclude passwords
    participant_data = [
        {
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "created_at": p.created_at
        }
        for p in participants
    ]

    return {
        "status": "success",
        "admin_id": admin.admin_id,
        "participants": participant_data
    }