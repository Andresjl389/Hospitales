from uuid import UUID
from domain.models.evaluations.questionnaire import Questionnaire
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class QuestionnaireRepository(BaseRepository[Questionnaire]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Questionnaire)
        
    def get_by_training_id(self, training_id: UUID):
        return self.db.query(Questionnaire).filter(Questionnaire.training_id == training_id).first()