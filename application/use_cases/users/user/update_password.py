from fastapi import HTTPException
from application.ports.users.user_port import IUserRepository
from core.security import check_password_hash, get_password_hash


class UpdateUserPassword:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, user_id: str, new_password: str, last_password: str = None):
        user = self.repo.get_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not check_password_hash(last_password, user.password):
            raise HTTPException(status_code=400, detail="Last password does not match")

        user.password = get_password_hash(new_password)  # In a real scenario, hash the password before saving
        self.repo.update(user)
        raise HTTPException(status_code=200, detail="Password updated successfully")