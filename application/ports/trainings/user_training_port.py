from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.trainings.user_training import UserTraining


class IUserTrainingRepository(IBaseRepository[UserTraining]):
    def get_by_user_and_assignment(user_id: UUID, assignment_id: UUID): ...
    
    def get_by_user(self, user_id: UUID): ...