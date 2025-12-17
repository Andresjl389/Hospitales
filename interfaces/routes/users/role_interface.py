from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from application.schemas.users.role_schema import RoleSchema
from application.use_cases.users.role.get_list_roles import ListRoles
from core.config import get_db
from core.security import require_role
from domain.models.users.user import User
from infrastructure.repositories.users.role_repository import RoleRepository


role_router = APIRouter(
    prefix='/roles',
    tags=['Roles']
)


@role_router.get("", response_model=list[RoleSchema])
def list_roles(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = RoleRepository(db)
    use_case = ListRoles(repo)
    return use_case.execute()
