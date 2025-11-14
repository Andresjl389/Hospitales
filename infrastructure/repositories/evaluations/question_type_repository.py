from uuid import UUID
from domain.models.evaluations.question import Question
from domain.models.evaluations.question_type import QuestionType
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class QuestionTypeRepository(BaseRepository[QuestionType]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, QuestionType)