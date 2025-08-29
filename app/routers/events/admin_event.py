from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.auth_models import EventIn
from app.database import get_sql_session
from app.services.create_event_service import create_event_service
from app.routers.admin.admin_dashboard import get_current_admin_id, verify_admin_exists

router = APIRouter(prefix="/admin/event", tags=["Admin Events"])

@router.post("/createEvent")
async def create_event(
    event: EventIn,
    db: AsyncSession = Depends(get_sql_session),
):

    # ✅ Create event
    new_event = await create_event_service(event, db)
    return {"message": "Event created successfully", "event_id": new_event.eid}