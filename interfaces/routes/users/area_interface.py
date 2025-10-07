from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from application.schemas.users.area_schema import AreaSchema, CreateAreaSchema
from application.use_cases.users.area.create_area import CreateArea
from application.use_cases.users.area.delete_user import DeleteArea
from application.use_cases.users.area.get_area import GetArea
from application.use_cases.users.area.get_list_areas import ListAreas
from application.use_cases.users.area.update_area import UpdateArea
from core.config import get_db
from core.security import require_role
from domain.models.users.user import User
from infrastructure.repositories.users.area_repository import AreaRepository


area_router = APIRouter(
    prefix='/areas',
    tags=['Areas']
)

@area_router.get("", response_model=list[AreaSchema])
def get_list_areas(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AreaRepository(db)
    use_case = ListAreas(repo)
    return use_case.execute()


@area_router.get("/{area_id}", response_model=AreaSchema)
def get_area(area_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AreaRepository(db)
    use_case = GetArea(repo)
    return use_case.execute(area_id)

@area_router.post("", response_model=AreaSchema)
def create_area(area: CreateAreaSchema, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AreaRepository(db)
    use_case = CreateArea(repo)
    return use_case.execute(area)

@area_router.put("/{area_id}", response_model=AreaSchema)
def update_area(area_id: UUID, area: CreateAreaSchema, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AreaRepository(db)
    use_case = UpdateArea(repo)
    return use_case.execute(area_id, area)

@area_router.delete("/{area_id}", response_model=AreaSchema)
def delete_area(area_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AreaRepository(db)
    use_case = DeleteArea(repo)
    return use_case.execute(area_id)