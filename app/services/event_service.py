from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.event_models import Event  # your Event model

async def get_all_events_service(db: AsyncSession):
    result = await db.execute(select(Event).where(Event.is_live.is_(True)))
    return result.scalars().all()
