from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.participant_models import Participant
from app.database import get_sql_session
from starlette.templating import Jinja2Templates
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def dashboard(request: Request, db: AsyncSession = Depends(get_sql_session)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    result = await db.execute(select(Participant).where(Participant.id == user_id))
    user = result.scalar_one_or_none()

    if user:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": user
        })
    else:
        raise HTTPException(status_code=404, detail="User not found")
