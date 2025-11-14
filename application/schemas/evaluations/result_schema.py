from datetime import date
from uuid import UUID
from pydantic import BaseModel

class ResultCreate(BaseModel):
    questionnaire_id: UUID  # único dato necesario

class ResultResponse(BaseModel):
    id: UUID
    score: int
    status: str
    created_at: date
    user_id: UUID
    questionnaire_id: UUID

    class Config:
        from_attributes = True
