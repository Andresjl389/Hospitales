from domain.models.trainings.training import Training
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class TrainingRepository(BaseRepository[Training]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Training)