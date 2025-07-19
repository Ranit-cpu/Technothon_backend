# app/routers/event/admin_event.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
#from sqlalchemy.orm import Session

from app.models.auth_models import EventIn
from app.database import get_sql_session
from app.services.create_event_service import create_event_service

router = APIRouter(prefix="/admin/event", tags=["Admin Events"])

@router.post("/createEvent")
async def create_event(event: EventIn, db: AsyncSession = Depends(get_sql_session)):

    await create_event_service(event, db)
    return {"message": "Event created successfully"}

