# application/use_cases/users/logout_user.py
from fastapi import Response
from application.ports.users.user_port import IUserRepository
from domain.models.users.user import User
from core.config import settings

class LogoutUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, current_user: User, response: Response) -> dict:
        # ❌ eliminar refresh tokens en la DB
        self.repo.delete_refresh_token(current_user.id)

        # ❌ eliminar la cookie de refresh_token en el navegador
        cookie_opts = {
            "httponly": True,
            "secure": settings.COOKIE_SECURE,
            "samesite": settings.COOKIE_SAMESITE,
            "domain": settings.COOKIE_DOMAIN
        }
        response.delete_cookie(
            key="refresh_token",
            **cookie_opts
        )
        response.delete_cookie(
            key="access_token",
            **cookie_opts
        )

        return {"msg": "Sesión cerrada exitosamente"}
