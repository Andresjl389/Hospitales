from uuid import UUID
from application.ports.base_repository import IBaseRepository
from domain.models.evaluations.result import Result


class IResultRepository(IBaseRepository[Result]): ...
    