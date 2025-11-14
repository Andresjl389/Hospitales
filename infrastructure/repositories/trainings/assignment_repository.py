from uuid import UUID
from domain.models.trainings.assignment import Assignment
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload


class AssignmentRepository(BaseRepository[Assignment]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Assignment)
    
    def get_by_area(self, area_id: str):
        return (
            self.db.query(Assignment)
            .options(
                joinedload(Assignment.trainings), 
                joinedload(Assignment.area),
                joinedload(Assignment.status)
            )
            .filter(Assignment.id_area == area_id)
            .all()
        )
        
    def get_by_area_and_training(self, area_id: UUID, training_id: UUID):
        return (
            self.db.query(Assignment)
            .options(
                joinedload(Assignment.trainings),
                joinedload(Assignment.area),
                joinedload(Assignment.status)
            )
            .filter(
                Assignment.id_area == area_id,
                Assignment.training_id == training_id
            )
            .first()
        )