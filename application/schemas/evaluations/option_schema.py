from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from application.schemas.evaluations.question_schema import QuestionResponse


class OptionBase(BaseModel):
    is_correct: bool
    option_text: str
    
class OptionCreate(OptionBase):
    question_id: UUID
    
    
class OptionUpdate(BaseModel):
    is_correct: Optional[bool] = None
    option_text: Optional[str] = None
    question_id: Optional[UUID] = None
    
class OptionResponse(OptionBase):
    id: UUID
    questions: QuestionResponse
    
