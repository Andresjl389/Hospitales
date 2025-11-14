import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class SatisfactionSurvey(Base):
    __tablename__ = "satisfaction_surveys"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    rating = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="satisfaction_surveys")