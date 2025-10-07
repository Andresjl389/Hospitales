from uuid import UUID

from fastapi import HTTPException
from application.ports.users.refresh_token_port import IRefreshTokenRepository
from application.ports.users.user_port import IUserRepository


class DeleteUser:
    def __init__(self, user_repository: IUserRepository, refresh_token_repository: IRefreshTokenRepository):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        
    def execute(self, user_id: UUID):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.refresh_token_repository.delete_by_user_id(user_id)
        self.user_repository.delete(user_id)
        raise HTTPException(status_code=200, detail="User deleted successfully")