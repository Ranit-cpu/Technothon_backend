from celery.bin.result import result
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth_models import EventIn
from app.database import get_sql_session
from app.services.event_service import get_all_events_service
from app.routers.admin.admin_dashboard import get_current_admin_id, verify_admin_exists

router = APIRouter(prefix="", tags=["User Events"])

@router.get("/events")
async def get_all_events(db: AsyncSession = Depends(get_sql_session)):
    events = await get_all_events_service(db)
    print("Events fetched:", events)
    return [
        {
            "id": e.eid,
            "name": e.name,
            "description": e.description,
            "event_type": e.event_type,
            "start_date": str(e.start_date),
            "end_date": str(e.end_date),
            "prize_details": e.prize_details,
            "is_live": e.is_live
        }
        for e in events
    ]