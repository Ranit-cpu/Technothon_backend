from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey
from app.models.base import Base

class Gallery(Base):
    __tablename__ = 'gallery'

    image_id = Column(String(255), primary_key=True, index=True)
    description = Column(String(255), nullable=True)
    event_id = Column(Text, ForeignKey('events.eid'), nullable=False)
    image_path = Column(String(500), nullable=True)  # Store file path instead of binary data
    created_at = Column(DateTime, nullable=False)