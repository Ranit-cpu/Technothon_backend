from app.models.base import Base
from sqlalchemy import Column,String,ForeignKey, Boolean,Date,Text
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(255), primary_key=True)
    job_title = Column(String(255), nullable=False)
    job_description = Column(Text)
    domain_id = Column(String(255), ForeignKey("domains.domain_id"))
    is_live = Column(Boolean, default=True)
    end_date = Column(Date)

    # relationships
    # domain = relationship("Domain", back_populates="jobs")
    # applications = relationship("Application", back_populates="job")