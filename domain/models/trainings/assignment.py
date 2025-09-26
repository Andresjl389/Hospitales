import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    assignment_date = Column(Date, nullable=False)
    completed_date = Column(Date, nullable=True)
    id_user = Column(Uuid, ForeignKey("users.id"), nullable=False)
    id_status = Column(Uuid, ForeignKey("statuses.id"), nullable=False)
    training_id = Column(Uuid, ForeignKey("trainings.id"), nullable=False)

    user = relationship("User", back_populates="assignments")
    statuses = relationship("Status", back_populates="assignments")
    trainings = relationship("Training", back_populates="assignments")