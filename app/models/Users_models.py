from sqlalchemy import Column, String, BigInteger, Numeric, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    Student_ID = Column(BigInteger, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    id = Column(String(100), nullable=False)
    Batch = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    OverAll_Percentage = Column(Numeric(5, 2), nullable=False)
    created_at = Column(DateTime)
