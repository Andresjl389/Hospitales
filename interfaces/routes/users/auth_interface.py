# interfaces/users/user_interface.py
from fastapi import APIRouter, Cookie, Depends, Request, Response
from sqlalchemy.orm import Session
from application.schemas.users.user_schema import UserLogin, UserSchema
from application.use_cases.users.auth.login_user import LoginUser
from application.use_cases.users.auth.logout_user import LogoutUser
from application.use_cases.users.auth.refresh_access_token import RefreshAccessToken
from core.config import get_db
from core.security import get_current_user
from domain.models.users.user import User
from infrastructure.repositories.users.user_repository import UserRepository

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@auth_router.post("/login")
def login_user(user: UserLogin, response: Response, request: Request, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    use_case = LoginUser(repo)
    return use_case.execute(user, response, request)

@auth_router.post("/refresh")
def refresh_token(
    response: Response,
    refresh_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    repo = UserRepository(db)
    use_case = RefreshAccessToken(repo)
    return use_case.execute(refresh_token, response)

@auth_router.post("/logout")
def logout_user(response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    use_case = LogoutUser(repo)
    return use_case.execute(current_user, response)

@auth_router.get("/me", response_model=UserSchema)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


