import asyncio
from app.database import engine_sqlite, engine_mysql
from app.models.base import Base_sqlite, Base
from app.models.sponsor_models import Sponsor  # Import Sponsor model
from app.models.Users_models import User
from app.models.team_models import Team
from app.models.event_models import Event
from app.models.payment_models import Payment
from app.models.admin_models import Admin
from app.models.participant_models import Participant

async def init_models():
    # Create SQLite tables
    async with engine_sqlite.begin() as conn:
        await conn.run_sync(Base_sqlite.metadata.create_all)
    print("SQLite tables created successfully!")
    
    # Create MySQL tables
    async with engine_mysql.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("MySQL tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
