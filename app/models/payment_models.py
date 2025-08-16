from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payments"

    transaction_id = Column(String, primary_key=True,unique=True, nullable=False)
    utr_no = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    upi_id = Column(String, nullable=False)
    payment_mode = Column(String, nullable=False)  # ✅ new
    amount = Column(Float, nullable=False)  # ✅ new
    description = Column(String)  # ✅ new
    status = Column(String, default="PENDING")
    paid_at = Column(DateTime)