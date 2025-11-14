from uuid import UUID
from domain.models.evaluations.question import Question
from domain.models.evaluations.questionnaire import Questionnaire
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session, joinedload


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Question)
        
    def get_by_questionnaire_id(self, questionnaire_id: UUID) -> list[Question]:
        return self.db.query(Question).filter(Question.questionnaire_id == questionnaire_id).all()
    
    def get_by_training_id(self, training_id: UUID) -> list[Question]:
        return (
            self.db.query(Question)
            .join(Questionnaire, Question.questionnaire_id == Questionnaire.id)
            .filter(Questionnaire.training_id == training_id)
            .options(joinedload(Question.questionnaires))
            .all()
        )