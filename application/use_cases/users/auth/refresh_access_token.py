from datetime import datetime, timezone
from fastapi import HTTPException, Response
from application.ports.users.user_port import IUserRepository
from core.security import create_access_token, hash_token, ACCESS_TOKEN_EXPIRE_MINUTES
from core.config import settings

class RefreshAccessToken:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, refresh_token_value: str, response: Response) -> dict:
        """
        Genera un nuevo access_token usando el refresh_token de la cookie.
        Establece el nuevo access_token como cookie HttpOnly.
        """
        if not refresh_token_value:
            raise HTTPException(status_code=401, detail="No refresh token provided")

        refresh_hash = hash_token(refresh_token_value)
        token_entity = self.repo.get_refresh_token(refresh_hash)

        if not token_entity:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # 🔥 Usar timezone.utc en vez de datetime.utcnow() para consistencia
        
        if token_entity.expires_at.replace(tzinfo=None) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expired")

        # Generar nuevo access token
        new_access_token = create_access_token(token_entity.user_id)

        # 🔥 Establecer la cookie con el nuevo access_token
        cookie_opts = {
            "httponly": True,
            "secure": settings.COOKIE_SECURE,
            "samesite": settings.COOKIE_SAMESITE,
            "domain": settings.COOKIE_DOMAIN
        }

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            **cookie_opts,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        print(f"✅ Token refrescado para user_id: {token_entity.user_id}")

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
