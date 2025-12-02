# app/models/Students_models.py
from sqlalchemy import Column, String, BigInteger,Numeric,DateTime
from app.models.base import Base_sqlite

class Student(Base_sqlite):

    __tablename__ = "Students"

    Student_ID = Column(BigInteger, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Batch = Column(String(20), nullable=False)
    Overall_Percentage = Column(Numeric(5,2), nullable=False)