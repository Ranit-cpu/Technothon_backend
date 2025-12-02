from sqlalchemy import Column, String, BigInteger, LargeBinary, DateTime, Text
from app.models.base import Base
from datetime import datetime

class Sponsor(Base):
    __tablename__ = "sponsors"

    sponsor_id = Column(String(255), primary_key=True,unique=True, nullable=False)
    sponsor_name = Column(String(255), nullable=False)
    selling_domain = Column(String(255), nullable=False)
    given_amount = Column(BigInteger, nullable=True)  # Optional - can be NULL if providing goods
    goods_services = Column(Text, nullable=True)  # Description of goods/services provided
    contribution_type = Column(String(50), nullable=False)  # 'monetary', 'goods', or 'both'
    sponsor_logo = Column(LargeBinary, nullable=True)  # For binary encoded photos
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
