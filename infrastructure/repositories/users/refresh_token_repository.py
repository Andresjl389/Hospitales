
from sqlalchemy.orm import Session
from domain.models.users.refresh_token import RefreshToken
from domain.models.users.role import Role
from infrastructure.repositories.base_repository import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, RefreshToken)

    def delete_by_user_id(self, user_id: str) -> None:
        self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        self.db.commit()
