
from sqlalchemy.orm import Session

from domain.models.users.refresh_token import RefreshToken
from domain.models.users.user import User
from infrastructure.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, User)

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def delete_refresh_token(self, user_id: str) -> None:
        self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        self.db.commit()
        
    def get_refresh_token(self, token_hash: str) -> RefreshToken:
        return self.db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    
    def get_by_cedula(self, cedula: str):
        return self.db.query(User).filter(User.cedula == cedula).first()