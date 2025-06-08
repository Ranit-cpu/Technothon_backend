from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.models.participant_models import Participant
from app.database import get_session

router = APIRouter()

@router.get("/dashboard")
async def dashboard(request: Request, db: AsyncSession = Depends(get_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    user = db.query(Participant).filter(Participant.id == user_id).first()

    if user:
        return {
            "status": "success",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at
            }
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
