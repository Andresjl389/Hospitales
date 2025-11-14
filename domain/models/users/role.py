import uuid
from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    name = Column(String, index=True, nullable=False)
    
    users = relationship("User", back_populates="role", cascade="all, delete-orphan")