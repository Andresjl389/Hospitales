import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    training_id = Column(Uuid, ForeignKey("trainings.id", ondelete='CASCADE'), nullable=False)
    
    trainings = relationship("Training", back_populates="questionnaires")
    questions = relationship("Question", back_populates="questionnaires", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="questionnaire", cascade="all, delete-orphan")
    
