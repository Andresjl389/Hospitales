from datetime import datetime
from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from application.ports.trainings.status_port import IStatusRepository
from application.schemas.trainings.assignment_schema import AssignmentUpdate
from domain.models.trainings.assignment import Assignment


class UpdateAssignment:
    def __init__(self, repository: IAssignmentRepository, status_repository: IStatusRepository):
        self.repository = repository
        self.status_repository = status_repository
        
    def execute(self, assignment_id, update_data: AssignmentUpdate) -> Assignment:
        assignment = self.repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        
        if update_data.id_status:
            status = self.status_repository.get_by_id(update_data.id_status)
            if not status:
                raise HTTPException(status_code=404, detail="Status not found")
            if status.name == "Completed" or status.name == "Expired":
                update_data.completed_date = update_data.completed_date or datetime.today().date()
            assignment.id_status = update_data.id_status
            update_data.completed_date = None
        
        if update_data.completed_date is not None:
            assignment.completed_date = update_data.completed_date
            
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(assignment, key, value)
            
        self.repository.update(assignment)
        return assignment