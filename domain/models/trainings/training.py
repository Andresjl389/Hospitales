import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    url_video = Column(String, nullable=False)
    url_image = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="trainings")
    assignments = relationship("Assignment", back_populates="trainings")
    questionnaires = relationship("Questionnaire", back_populates="trainings")