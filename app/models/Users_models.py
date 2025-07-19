# app/models/Users_models.py
from sqlalchemy import Column, String, DateTime
from app.models.base import Base  # ✅ This is correct

class User(Base):
    __tablename__ = "users"

    uid = Column(String(100), primary_key=True, index=True)
    Student_ID = Column(String(100), unique=True, nullable=False)
    Name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime)
    email = Column(String(100), nullable=False)
