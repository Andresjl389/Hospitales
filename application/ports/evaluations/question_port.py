from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.evaluations.question import Question


class IQuestionRepository(IBaseRepository[Question]):
    def get_by_questionnaire_id(self, questionnaire_id: UUID) -> list[Question]: ...
    
    def get_by_training_id(self, training_id: UUID) -> list[Question]: ...