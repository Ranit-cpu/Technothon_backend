# app/models/participant_models.py
from sqlalchemy import Column, String, ForeignKey
from app.models.base import Base

class Participant(Base):
    __tablename__ = "participants"

    pid = Column(String(10), primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    user_id = Column(String(100), ForeignKey('users.uid'),nullable=False,)
    team_id = Column(String(100), ForeignKey('teams.tid'))
    event_id = Column(String(100), ForeignKey('events.eid'))
    role = Column(String(50), nullable=False)
