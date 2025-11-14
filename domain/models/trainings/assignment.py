from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    assignment_date = Column(Date, nullable=False, default=datetime.now(timezone.utc))
    completed_date = Column(Date, nullable=True)
    id_area = Column(Uuid, ForeignKey("areas.id"), nullable=False)
    id_status = Column(Uuid, ForeignKey("statuses.id"), nullable=False)
    training_id = Column(Uuid, ForeignKey("trainings.id"), nullable=False)

    area = relationship("Area", back_populates="assignments")
    status = relationship("Status", back_populates="assignments")
    trainings = relationship("Training", back_populates="assignments")