from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from application.schemas.trainings.status_schema import StatusSchema
from application.schemas.trainings.training_schema import TrainingResponse
from application.schemas.users.area_schema import AreaSchema


class AssignmentBase(BaseModel):
    id_area: UUID
    training_id: UUID
    
class AssignmentUpdate(BaseModel):
    id_status: Optional[UUID] = None
    id_area: Optional[UUID] = None
    training_id: Optional[UUID] = None
    completed_date: Optional[date] = None

class AssignmentResponse(BaseModel):
    id: UUID
    assignment_date: date
    completed_date: date | None
    area: AreaSchema
    trainings: TrainingResponse
    status: StatusSchema