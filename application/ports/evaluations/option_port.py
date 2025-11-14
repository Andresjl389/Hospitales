from typing import Optional
from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.evaluations.option import Option
from domain.models.evaluations.question import Question


class IOptionRepository(IBaseRepository[Option]):
    def get_correct_option_by_question(self, question_id: UUID) -> Optional[Option]: ...
    
    def get_by_id_question(self, question_id: UUID) -> list[Option] :...