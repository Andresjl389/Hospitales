from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TrainingBase(BaseModel):
    title: str
    description: Optional[str] = None

class TrainingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    # Si necesitas area_id, agrégalo aquí:
    # area_id: Optional[UUID] = None

class TrainingResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    url_video: Optional[str] = None
    url_image: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True