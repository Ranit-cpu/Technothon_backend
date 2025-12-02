from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"

    transaction_id = Column(String(255), primary_key=True, index=True)
    utr_no = Column(String(255), nullable=True)
    bank_name = Column(String(255), nullable=True)
    upi_id = Column(String(255), nullable=True)
    paid_at = Column(DateTime)
    status = Column(String(20), default="PENDING")