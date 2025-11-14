from uuid import UUID
from domain.models.trainings.assignment import Assignment
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class AssignmentRepository(BaseRepository[Assignment]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Assignment)
    
    def get_by_area(self, area_id: UUID) -> Assignment:
        return self.db.query(Assignment).filter(Assignment.id_area == area_id).all()