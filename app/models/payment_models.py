from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"
    
    transaction_id = Column(String(255), primary_key=True, nullable=False)
    utr_no = Column(String(255), nullable=True)
    bank_name = Column(String(255), nullable=True)
    upi_id = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True, server_default=func.current_timestamp())