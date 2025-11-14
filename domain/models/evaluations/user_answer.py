import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    answer_date = Column(Date, nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    question_id = Column(Uuid, ForeignKey("questions.id", ondelete='CASCADE'), nullable=False)
    option_id = Column(Uuid, ForeignKey("options.id", ondelete='CASCADE'), nullable=True)
    
    user = relationship("User", back_populates="user_answers")
    questions = relationship("Question", back_populates="user_answers")
    options = relationship("Option", back_populates="user_answers")

