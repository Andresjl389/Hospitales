from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from application.schemas.evaluations.question_type_schema import QuestionTypeBase
from application.schemas.evaluations.questionaire_schema import QuestionnaireResponse


class QuestionBase(BaseModel):
    question_text: str
    question_type_id: UUID
    questionnaire_id: UUID
    
class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type_id: Optional[UUID] = None
    questionnaire_id: Optional[UUID] = None
    
class QuestionShortResponse(BaseModel):
    question_text: str
    
class QuestionResponse(BaseModel):
    id: UUID
    question_text: str
    question_types: QuestionTypeBase
    questionnaires: QuestionnaireResponse

    class Config:
        from_attributes = True