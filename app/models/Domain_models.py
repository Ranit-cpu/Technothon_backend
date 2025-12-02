from app.models.base import Base
# from sqlalchemy.orm import relationship
from sqlalchemy import Column,String

class Domain(Base):
    __tablename__ = 'domains'

    domain_id = Column(String(255), primary_key=True)
    domain_name = Column(String(255), unique=True, nullable=False)

    # relationships
    # jobs = relationship("Job", back_populates="domain", cascade="all, delete-orphan")
    # applications = relationship("Application", back_populates="domain", cascade="all, delete-orphan")