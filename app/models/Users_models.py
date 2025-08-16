from sqlalchemy import Column, String, DateTime, Integer
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String(255), primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    Batch = Column(String(100), nullable=True)
    Phone_No = Column(String(20), nullable=True)
    Whatsapp_No = Column(String(20), nullable=True)
    Overall_Percentage = Column(Integer, nullable=True)
    Student_ID = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime)
