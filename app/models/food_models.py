from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, LargeBinary
from app.models.base import Base

class Food(Base):
    __tablename__ = 'food_coupons'

    coupon_id = Column(String(255), primary_key=True, index=True)
    pid=Column(String(100), ForeignKey('participants.pid'))
    food_preference=Column(String(255), nullable=False, default='Veg')
    flag=Column(Integer, nullable=False, default=0)
    issued_at = Column(DateTime, nullable=False)