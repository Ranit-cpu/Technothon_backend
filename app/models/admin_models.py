from sqlalchemy import Column, String, Text
from app.models.base import Base

class Admin(Base):
    __tablename__ = "admins"
    
    # Define columns first
    admin_id = Column(String(11), index=True)
    password = Column(String(255), nullable=False)
    
    # Tell SQLAlchemy to treat admin_id as primary key for ORM purposes
    __mapper_args__ = {
        'primary_key': (admin_id,)
    }