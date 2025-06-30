import asyncio
from app.database import engine
from app.models.participant_models import Base  # Import your Base with all models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Creates tables if they don't exist

if __name__ == "__main__":
    asyncio.run(init_models())
