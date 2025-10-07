from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from domain.models.trainings.assignment import Assignment


class ListAssignments:
    def __init__(self, repository: IAssignmentRepository):
        self.repository = repository
        
    def execute(self) -> Assignment:
        assignment = self.repository.get_all()
        if not assignment:
            raise HTTPException(status_code=404, detail="No assignments found")
        return assignment