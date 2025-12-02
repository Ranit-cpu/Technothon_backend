# app/models/event_models.py
from sqlalchemy import Column, String, Date, Text
from sqlalchemy.dialects.mssql import TINYINT
from app.models.base import Base

class Event(Base):
    __tablename__ = "events"

    eid = Column(String(100), primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    prize_details = Column(Text)
    is_live = Column(TINYINT, default=False)
