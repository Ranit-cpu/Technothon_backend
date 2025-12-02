from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract
from sqlalchemy.future import select
from app.models.event_models import Event
from app.database import get_sql_session
from app.services.event_service import get_all_events_service
from datetime import date

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
            "year": e.start_date.year,
            "prize_details": e.prize_details,
            "is_live": e.is_live
        }
        for e in events
    ]

@router.get("/events/{year}")
async def get_event_by_year(year: int, db: AsyncSession = Depends(get_sql_session)):
    today = date.today()

    stmt = (
        select(Event)
        .where(
            extract("year", Event.start_date) == year,
            Event.is_live == 1,
            Event.start_date <= today,
            Event.end_date >= today
        )
    )

    result = await db.execute(stmt)
    events = result.scalars().all()

    if not events:
        raise HTTPException(status_code=404, detail=f"No active events found for year {year}")

    return {
        "events": [
            {
                "id": e.eid,
                "name": e.name,
                "description": e.description,
                "event_type": e.event_type,
                "start_date": str(e.start_date),
                "end_date": str(e.end_date),
                "prize_details": e.prize_details,
                "is_live": e.is_live,
            }
            for e in events
        ]
    }

# NEW ROUTE: Get event status by name and year
@router.get("/event-status/{event_name}/{year}")
async def get_event_status(event_name: str, year: int, db: AsyncSession = Depends(get_sql_session)):
    """
    Get event live status by event name and year
    event_name: 'IoT-Exposition' or 'AI-Unleashed'
    """
    stmt = select(Event).where(
        extract("year", Event.start_date) == year,
        Event.name == event_name
    )
    
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(
            status_code=404, 
            detail=f"{event_name} not found for year {year}"
        )
    
    return {
        "event_name": event.name,
        "year": year,
        "is_live": event.is_live,
        "start_date": str(event.start_date),
        "end_date": str(event.end_date)
    }