from datetime import datetime
from fastapi import HTTPException, Response, Cookie
from application.ports.users.user_port import IUserRepository
from core.security import create_access_token, hash_token, ACCESS_TOKEN_EXPIRE_MINUTES

class RefreshAccessToken:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, refresh_token_value: str) -> dict:
        if not refresh_token_value:
            raise HTTPException(status_code=401, detail="No refresh token provided")

        refresh_hash = hash_token(refresh_token_value)
        token_entity = self.repo.get_refresh_token(refresh_hash)

        if not token_entity:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        if token_entity.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Generar nuevo access token
        new_access_token = create_access_token(token_entity.user_id)

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
