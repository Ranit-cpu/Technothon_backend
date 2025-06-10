from sqlalchemy import Column, String,Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"

    #name = Column(String(100), nullable=False)
    admin_id = Column(String(11), primary_key=True,index=True)
    password = Column(String(255),nullable=False)
    privileges = Column(Text)

    def __repr__(self):
        return (
            f"‹Admin(name={self.name}, email={self.email}, role {self.role}, "
            f"department={self.department}, designation={self.designation})>"
        )
