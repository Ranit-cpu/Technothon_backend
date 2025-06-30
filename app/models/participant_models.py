# app/models/participant_models.py
from sqlalchemy import Column, String, DateTime,Integer,Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Participant(Base):
    __tablename__ = "participants"

    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(200),nullable=False)
    created_at = Column(DateTime)
    studentID = Column(Integer, unique=True, nullable=False)
    leader = Column(Boolean, default= False)