from application.ports.base_repository import IBaseRepository
from domain.models.trainings.training import Training


class ITrainingRepository(IBaseRepository[Training]):
    pass