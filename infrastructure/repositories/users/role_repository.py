
from sqlalchemy.orm import Session
from domain.models.users.role import Role
from infrastructure.repositories.base_repository import BaseRepository

class RoleRepository(BaseRepository[Role]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, Role)

    def get_by_name(self, name: str):
        return self.db.query(Role).filter(Role.name == name).first()
