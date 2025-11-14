from datetime import date
from uuid import UUID
from pydantic import BaseModel
from application.schemas.evaluations.option_schema import OptionBase
from application.schemas.evaluations.question_schema import QuestionShortResponse
from application.schemas.trainings.training_schema import TrainingResponse
from application.schemas.users.user_schema import UserShortInfo


class UserAnswerBase(BaseModel):
    answer_date: date
    
class UserAnswerCreate(BaseModel):
    question_id: UUID
    option_id: UUID | None = None  # Para respuesta única
    option_ids: list[UUID] | None = None  # Para selección múltiple

class UserAnswerBulkCreate(BaseModel):
    """Para crear múltiples respuestas de una vez"""
    question_id: UUID
    option_ids: list[UUID]
    
class UserAnswerResponse(UserAnswerBase):
    id: UUID
    user: UserShortInfo
    questions: QuestionShortResponse
    options: OptionBase
    

    class Config:
        from_attributes = True