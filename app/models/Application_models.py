from app.models.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(String(255), primary_key=True)
    user_id = Column(String(255), ForeignKey("users.uid"), nullable=False)
    domain_id = Column(String(255), ForeignKey("domains.domain_id"), nullable=False)
    job_id = Column(String(255), ForeignKey("jobs.job_id"), nullable=True)
    full_name = Column(String(255))
    academic_batch = Column(String(100))
    student_id = Column(String(100))
    phone_number = Column(String(20))
    email_address = Column(String(255))
    resume_link = Column(String(500))
    github_link = Column(String(500))
    skills = Column(String(500))
    experience = Column(Text)
    reason = Column(String(500))
    applied_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    # domain = relationship("Domain", back_populates="applications")
    # job = relationship("Job", back_populates="applications")