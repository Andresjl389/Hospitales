from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from application.schemas.trainings.user_training_schema import UserTrainingCreate, UserTrainingResponse, UserTrainingUpdate
from application.use_cases.trainings.user_training.create_user_training import CreateUserTraining
from application.use_cases.trainings.user_training.get_user_training import GetUserTraining
from application.use_cases.trainings.user_training.update_user_training import UpdateUserTraining
from core.config import get_db
from core.security import get_current_user, require_role
from domain.models.users.user import User
from infrastructure.repositories.trainings.assignment_repository import AssignmentRepository
from infrastructure.repositories.trainings.status_repository import StatusRepository
from infrastructure.repositories.trainings.user_training_repository import UserTrainingRepository
from infrastructure.repositories.users.area_repository import AreaRepository
from infrastructure.repositories.users.user_repository import UserRepository
from infrastructure.storage.filesystem_storage import FileSystemStorageAdapter


user_training_router = APIRouter(
    prefix='/user_trainings',
    tags=['User Trainings']
)

@user_training_router.post('/{id_assignment}')
async def create_user_training(
    id_assignment: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin"]))
):
    repo = UserTrainingRepository(db)
    status_repo = StatusRepository(db)
    area_repo = AreaRepository(db)
    assignment_repo = AssignmentRepository(db)
    user_repo = UserRepository(db)
    use_case = CreateUserTraining(
        repo,
        status_repo,
        area_repo,
        assignment_repo,
        user_repo
    )
    return use_case.execute(id_assignment)

@user_training_router.get('', response_model=list[UserTrainingResponse])
async def get_user_training(
    request: Request,
    id_user_training: Optional[UUID] = None,
    id_user: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = UserTrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = GetUserTraining(repo, storage, request)
    return use_case.execute(id_user_training, id_user)

@user_training_router.put('/{id_user_training}')
async def update_user_training(
    id_user_training: UUID,
    user_training_data: UserTrainingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = UserTrainingRepository(db)
    status_repo = StatusRepository(db)
    assignment_repo = AssignmentRepository(db)
    use_case = UpdateUserTraining(repo, status_repo, assignment_repo)
    return use_case.execute(id_user_training, user_training_data)
    
    