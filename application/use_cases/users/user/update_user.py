from uuid import UUID

from fastapi import HTTPException
from application.ports.users.user_port import IUserRepository
from application.schemas.users.user_schema import UserUpdate
from domain.models.users.user import User


class UpdateUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, user_id: UUID, user_data: UserUpdate) -> User:
        existing_user = self.repo.get_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(existing_user, key, value)

        return self.repo.update(existing_user)