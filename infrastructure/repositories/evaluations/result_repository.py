
from domain.models.evaluations.result import Result
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class ResultRepository(BaseRepository[Result]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Result)
        