# application/use_cases/users/logout_user.py
from fastapi import Response
from application.ports.users.user_port import IUserRepository
from domain.models.users.user import User

class LogoutUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, current_user: User, response: Response) -> dict:
        # ❌ eliminar refresh tokens en la DB
        self.repo.delete_refresh_token(current_user.id)

        # ❌ eliminar la cookie de refresh_token en el navegador
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=False,   # cámbialo a True en producción con HTTPS
            samesite="strict"   
        )
        response.delete_cookie(
            key="access_token",
            httponly=True,
            secure=False,   # cámbialo a True en producción con HTTPS
            samesite="strict"   
        )

        return {"msg": "Sesión cerrada exitosamente"}
