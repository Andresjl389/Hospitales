from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.evaluations.questionnaire import Questionnaire


class IQuestionnaireRepository(IBaseRepository[Questionnaire]):
    def get_by_training_id(self, training_id: UUID): ...