from uuid import UUID

from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository


class DeleteAssignment:
    def __init__(self, repository: IAssignmentRepository):
        self.repository = repository
        
    def execute(self, assignment_id: UUID):
        assignment = self.repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        self.repository.delete(assignment.id)
        raise HTTPException(status_code=200, detail="Assignment deleted successfully")