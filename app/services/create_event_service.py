# app/services/event_service.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_models import Event
from app.models.auth_models import EventIn
from sqlalchemy import func
from sqlalchemy import select


async def create_event_service(event: EventIn, db: AsyncSession):
    event_id = await generate_event_code(db)  # now await this

    new_event = Event(
        eid=event_id,
        name=event.name,
        description=event.description,
        event_type=event.event_type,
        start_date=event.start_date,
        end_date=event.end_date,
        prize_details=event.prize_details,
        is_live=event.is_live
    )
    db.add(new_event)
    try:
        await db.commit()
        await db.refresh(new_event)  # optional, but good to have
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to DB: {str(e)}")

    return new_event


async def generate_event_code(db: AsyncSession) -> str:
    result = await db.execute(select(func.max(Event.eid)))
    max_id_str = result.scalar()
    
    if max_id_str:
        try:
            # Extract number part after 'TT' and increment
            max_num = int(max_id_str.replace("TT", ""))
        except ValueError:
            max_num = 0
    else:
        max_num = 0

    new_id = f"TT{max_num + 1:02d}"  # e.g., TT01, TT02, ..., TT99
    return new_id
