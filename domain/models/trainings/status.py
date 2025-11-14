import uuid
from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Status(Base):
    __tablename__ = "statuses"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    name = Column(String, index=True, nullable=False)
    
    assignments = relationship("Assignment", back_populates="status")
    user_trainings = relationship("UserTraining", back_populates="status")