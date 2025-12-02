from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Boolean
from datetime import datetime
from app.models.base import Base

class Team(Base):
    __tablename__ = 'teams'

    tid = Column(String(100), primary_key=True)
    name = Column(String)
    idea_title = Column(String)
    idea_description = Column(Text)
    event_id = Column(Text)
    created_by = Column(String(100), ForeignKey('participants.pid'))
    transaction_id = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # ✅ New column to track registration/approval status
    registered = Column(Boolean, default=False)
