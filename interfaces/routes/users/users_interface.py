from uuid import UUID
from fastapi import APIRouter, Depends
from application.schemas.users.user_schema import UserCreate, UserSchema, UserUpdate
from sqlalchemy.orm import Session
from application.use_cases.users.user.create_user import CreateUser
from application.use_cases.users.user.delete_user import DeleteUser
from application.use_cases.users.user.get_list_users import ListUsers
from application.use_cases.users.user.get_user import GetUser
from application.use_cases.users.user.update_password import UpdateUserPassword
from application.use_cases.users.user.update_user import UpdateUser
from core.config import get_db
from core.security import require_role, get_current_user
from domain.models.users.user import User
from infrastructure.repositories.users.area_repository import AreaRepository
from infrastructure.repositories.users.refresh_token_repository import RefreshTokenRepository
from infrastructure.repositories.users.role_repository import RoleRepository
from infrastructure.repositories.users.user_repository import UserRepository


user_router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@user_router.post("", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = UserRepository(db)
    role_repo = RoleRepository(db)
    area_repo = AreaRepository(db)
    use_case = CreateUser(repo, role_repo, area_repo)
    return use_case.execute(user)

@user_router.get("", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = UserRepository(db)
    use_case = ListUsers(repo)
    return use_case.execute()

@user_router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = UserRepository(db)
    use_case = GetUser(repo)
    return use_case.execute(user_id)

@user_router.put("/{user_id}", response_model=UserSchema)
def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    use_case = UpdateUser(repo)
    return use_case.execute(user_id, user)


@user_router.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = UserRepository(db)
    refresh_token_repo = RefreshTokenRepository(db)
    use_case = DeleteUser(repo, refresh_token_repo)
    return use_case.execute(user_id)

@user_router.put("/{user_id}/password")
def update_user_password(user_id: UUID, new_password: str, last_password: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = UserRepository(db)
    use_case = UpdateUserPassword(repo)
    return use_case.execute(user_id, new_password, last_password)