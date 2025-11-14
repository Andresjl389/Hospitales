from uuid import UUID
from pydantic import BaseModel
from application.schemas.trainings.training_schema import TrainingResponse


class QuestionnaireBase(BaseModel):
    training_id: UUID
    
class QuestionnaireResponse(BaseModel):
    id: UUID
    trainings: TrainingResponse
    

    class Config:
        from_attributes = True