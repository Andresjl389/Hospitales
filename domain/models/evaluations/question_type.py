import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    name = Column(String, nullable=False)
    
    questions = relationship("Question", back_populates="question_types", cascade="all, delete-orphan")

