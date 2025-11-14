from fastapi import HTTPException
from application.ports.users.user_port import IUserRepository
from domain.models.users.user import User

class ListUsers:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self) -> list[User]:
        users = self.repo.get_all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users