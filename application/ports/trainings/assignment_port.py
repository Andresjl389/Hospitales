from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.trainings.assignment import Assignment


class IAssignmentRepository(IBaseRepository[Assignment]):
    def get_by_area(self, area_id: str) -> Assignment: ...
    
    def get_by_area_and_training(self, id_area: UUID, id_training: UUID) -> list[Assignment]: ...