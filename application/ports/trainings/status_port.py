from application.ports.base_repository import IBaseRepository
from domain.models.trainings.status import Status


class IStatusRepository(IBaseRepository[Status]):
    def get_by_name(self, name: str) -> Status: ...