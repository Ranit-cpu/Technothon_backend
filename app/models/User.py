# app/models/student.py
from sqlalchemy import Column, String, BigInteger,Numeric,Boolean
from sqlalchemy.orm import declarative_base

Base_sqlite = declarative_base()

class Student(Base_sqlite):

    __tablename__ = "students"

    Student_ID = Column(BigInteger, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Batch = Column(String(20), nullable=False)
    OverAll_Percentage = Column(Numeric(5,2), nullable=False)
    leader = Column(Boolean, default=False)