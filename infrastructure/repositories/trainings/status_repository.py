from domain.models.trainings.status import Status
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class StatusRepository(BaseRepository[Status]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Status)
        
    def get_by_name(self, name: str) -> Status:
        return self.db.query(Status).filter(Status.name == name).first()