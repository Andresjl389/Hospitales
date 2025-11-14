from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import Annotated, Optional
from pydantic import BaseModel, Field

from application.schemas.trainings.assignment_schema import AssignmentResponse
from application.schemas.trainings.status_schema import StatusSchema
from application.schemas.trainings.training_schema import TrainingResponse
from application.schemas.users.user_schema import UserSchema


class UserTrainingBase(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    progress: Annotated[Decimal, Field(max_digits=5, decimal_places=2, default=0.0)]
     
class UserTrainingCreate(UserTrainingBase):
    id_assignments: UUID
    id_training: UUID
    id_status: UUID
    
class UserTrainingUpdate(BaseModel):
    id_assignments: Optional[UUID] = None
    status: Optional[str] = None

class UserTrainingResponse(UserTrainingBase):
    id: UUID
    user: UserSchema
    assignments: AssignmentResponse
    trainings: TrainingResponse
    status: StatusSchema
    
    class Config:
        from_attributes = True
    