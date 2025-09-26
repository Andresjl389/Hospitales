import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    score = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    questionnaire_id = Column(Uuid, ForeignKey("questionnaires.id"), nullable=False)
    
    user = relationship("User", back_populates="results")
    questionnaire = relationship("Questionnaire", back_populates="results")
