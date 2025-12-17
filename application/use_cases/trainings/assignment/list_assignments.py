from application.ports.trainings.assignment_port import IAssignmentRepository
from domain.models.trainings.assignment import Assignment


class ListAssignments:
    def __init__(self, repository: IAssignmentRepository):
        self.repository = repository
        
    def execute(self) -> Assignment:
        assignment = self.repository.get_all()
        # When there are no assignments (e.g., fresh database) return an empty list
        # so consumers can render zero counts without failing the request.
        return assignment or []
