from typing import Optional
from uuid import UUID
from domain.models.evaluations.option import Option
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session

class OptionRepository(BaseRepository[Option]):
    
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Option)
        
    def get_correct_option_by_question(self, question_id: UUID) -> Optional[Option]:
        return self.db.query(Option).filter(
            Option.question_id == question_id,
            Option.is_correct == True
        ).first()
        
    def get_by_id_question(self, question_id: UUID) -> Option:
        return self.db.query(Option).filter(Option.question_id == question_id).all()
