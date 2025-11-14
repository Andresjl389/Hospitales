from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from application.ports.trainings.status_port import IStatusRepository
from application.schemas.trainings.assignment_schema import AssignmentBase
from domain.models.trainings.assignment import Assignment


class CreateAssignment:
    def __init__(self, repository: IAssignmentRepository, status_repository: IStatusRepository):
        self.repository = repository
        self.status_repository = status_repository
        
    def execute(self, assignment: AssignmentBase) -> Assignment:
        status = self.status_repository.get_by_name('Pending')
        if not status:
            raise HTTPException(status_code=404, detail="Status 'Pending' not found")
        
        new_assignment = Assignment(
            id_area=assignment.id_area,
            id_status=status.id,
            training_id=assignment.training_id,
            completed_date=None,
        )
        self.repository.create(new_assignment)
        return new_assignment