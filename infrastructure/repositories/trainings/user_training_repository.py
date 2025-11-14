from uuid import UUID
from domain.models.trainings.user_training import UserTraining
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class UserTrainingRepository(BaseRepository[UserTraining]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, UserTraining)
        
    def get_by_user_and_assignment(self, user_id: UUID, assignment_id: UUID):
        return (
            self.db.query(UserTraining)
            .filter(
                UserTraining.user_id == user_id,
                UserTraining.id_assignments == assignment_id
            )
            .first()
        )
        
    def get_by_user(self, user_id: UUID):
        return (
            self.db.query(UserTraining)
            .filter(UserTraining.user_id == user_id)
            .all()
        )

