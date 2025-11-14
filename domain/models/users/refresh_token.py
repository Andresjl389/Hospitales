# domain/models/users/refresh_token.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, String, Uuid
from sqlalchemy.orm import relationship
from core.config import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Uuid, primary_key=True, index=True, nullable=False, default=uuid.uuid4, unique=True)
    token_hash = Column(String, index=True, nullable=False)   # sha256 hex
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    user_agent = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    
    user = relationship("User", back_populates="refresh_tokens")

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expires_at
