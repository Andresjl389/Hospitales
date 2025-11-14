import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class UserTraining(Base):
    __tablename__ = "user_trainings"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    progress = Column(Numeric(5, 2), nullable=False, default=0.0)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    id_assignments = Column(Uuid, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    id_training = Column(Uuid, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False)
    id_status = Column(Uuid, ForeignKey("statuses.id"), nullable=False)
    
    
    status = relationship("Status", back_populates="user_trainings")
    user = relationship("User", back_populates="user_trainings")
    assignments = relationship("Assignment", back_populates="user_trainings")
    trainings = relationship("Training", back_populates="user_trainings")
    