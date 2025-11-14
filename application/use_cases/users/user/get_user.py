from uuid import UUID
from fastapi import HTTPException
from application.ports.users.user_port import IUserRepository
from domain.models.users.user import User

class GetUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, user_id: UUID) -> User | None:
        user = self.repo.get_by_id(user_id) 
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user