from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Response, Request
from application.ports.users.user_port import IUserRepository
from application.schemas.users.user_schema import UserLogin
from core.security import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, check_password_hash, create_access_token, generate_refresh_token_value, hash_token
from domain.models.users.refresh_token import RefreshToken
from domain.models.users.user import User

class LoginUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, data: UserLogin, response: Response, request: Request) -> dict:
        existing: User = self.repo.get_by_email(data.email)
        if not existing:
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        if not check_password_hash(data.password, existing.password):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        access_token = create_access_token(existing.id)
        refresh_value = generate_refresh_token_value()
        refresh_hash = hash_token(refresh_value)

        response.set_cookie(
            key="refresh_token",
            value=refresh_value,
            httponly=True,
            secure=False,       # ponlo en True cuando tengas HTTPS
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

        refresh_entity = RefreshToken(
            token_hash=refresh_hash,
            user_id=existing.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            user_agent=request.headers.get("user-agent"),  # ✅ instancia
            ip=request.client.host                         # ✅ instancia
        )
        self.repo.create_refresh_token(refresh_entity)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
