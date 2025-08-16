from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.participant_models import Participant
from app.models.Users_models import User
from app.database import get_sql_session
from app.models.team_models import Team

router = APIRouter()

@router.get("/dashboard")
async def dashboard(request: Request, db: AsyncSession = Depends(get_sql_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Get user information
    user_result = await db.execute(select(User).where(User.uid == user_id))
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get team info with payment status
    participant_result = await db.execute(
        select(Participant).where(Participant.user_id == user_id)
    )
    participant = participant_result.scalar_one_or_none()
    
    team = None
    if participant:
        team_result = await db.execute(
            select(Team).where(Team.tid == participant.team_id)
        )
        team = team_result.scalar_one_or_none()

    return {
        "user": user.__dict__ if user else None,
        "team": team.__dict__ if team else None
    }
    