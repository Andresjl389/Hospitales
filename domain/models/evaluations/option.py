import uuid
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Option(Base):
    __tablename__ = "options"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    is_correct = Column(Boolean, nullable=False)
    option_text = Column(String, nullable=False)
    question_id = Column(Uuid, ForeignKey("questions.id", ondelete='CASCADE'), nullable=False)
    
    questions = relationship("Question", back_populates="options")
    user_answers = relationship("UserAnswer", back_populates="options", cascade="all, delete-orphan")

