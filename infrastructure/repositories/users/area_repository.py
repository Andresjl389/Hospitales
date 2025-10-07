
from sqlalchemy.orm import Session
from domain.models.users.area import Area
from infrastructure.repositories.base_repository import BaseRepository

class AreaRepository(BaseRepository[Area]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Area)

    def get_by_name(self, name: str):
        return self.db.query(Area).filter(Area.name == name).first()
