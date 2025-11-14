import uuid
from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    name = Column(String, index=True, nullable=False)
    
    users = relationship("User", back_populates="area", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="area", cascade="all, delete-orphan")