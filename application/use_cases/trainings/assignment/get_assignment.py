from fastapi import HTTPException
from application.ports.trainings.assignment_port import IAssignmentRepository
from domain.models.trainings.assignment import Assignment


class GetAssignment:
    def __init__(self, repository: IAssignmentRepository):
        self.repository = repository

    def execute(self, area_id: str) -> Assignment:
        assignment = self.repository.get_by_area(area_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="No assignments found")
        return assignment