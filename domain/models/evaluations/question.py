import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    question_text = Column(String, nullable=False)
    question_type_id = Column(Uuid, ForeignKey("question_types.id", ondelete='CASCADE'), nullable=False)
    questionnaire_id = Column(Uuid, ForeignKey("questionnaires.id", ondelete='CASCADE'), nullable=False)
    
    question_types = relationship("QuestionType", back_populates="questions")
    questionnaires = relationship("Questionnaire", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="questions", cascade="all, delete-orphan")
    options = relationship("Option", back_populates="questions", cascade="all, delete-orphan")

