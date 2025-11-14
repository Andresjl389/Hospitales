from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.evaluations.question_type import QuestionType


class IQuestionTypeRepository(IBaseRepository[QuestionType]): ...