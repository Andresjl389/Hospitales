from fastapi import HTTPException
from application.ports.users.user_port import IUserRepository
from core.security import decode_access_token

class GetCurrentUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, token: str):
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return user
