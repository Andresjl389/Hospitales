# interfaces/routes/training_routes.py
from typing import List, Optional, Union
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, HTTPException
from sqlalchemy.orm import Session
from application.schemas.trainings.training_schema import TrainingBase, TrainingResponse, TrainingUpdate
from application.use_cases.trainings.training.create_training import CreateTraining
from application.use_cases.trainings.training.delete_training import DeleteTraining
from application.use_cases.trainings.training.get_list_training import GetListTrainings
from application.use_cases.trainings.training.get_training import GetTraining
from application.use_cases.trainings.training.update_training import UpdateTraining
from core.config import get_db
from core.security import require_role
from domain.models.users.user import User
from infrastructure.repositories.trainings.training_repository import TrainingRepository
from infrastructure.storage.filesystem_storage import FileSystemStorageAdapter
from interfaces.dependencies.users.user_dependencies import get_current_user


training_router = APIRouter(
    prefix='/trainings',
    tags=['Trainings']
)

@training_router.post('', response_model=TrainingResponse)
async def create_training(
        title: str = Form(...),
        description: str = Form(...),
        video: UploadFile = File(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["Admin"]))
    ):
    repository = TrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = CreateTraining(repository, storage)

    video_bytes = await video.read()
    image_bytes = await image.read()

    training_data = TrainingBase(
        title=title,
        description=description
    )

    training = use_case.execute(
        data=training_data,
        video_bytes=video_bytes,
        video_filename=video.filename,
        image_bytes=image_bytes,
        image_filename=image.filename,
        user_id=current_user.id
    )

    return training

@training_router.get("", response_model=List[TrainingResponse])
def list_trainings(
    request: Request,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repository = TrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = GetListTrainings(repository, storage, request)
    return use_case.execute()

@training_router.get("/{training_id}", response_model=TrainingResponse)
def get_training(
    training_id: UUID, 
    request: Request, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repository = TrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = GetTraining(repository, storage, request)
    return use_case.execute(training_id)

@training_router.put("/{training_id}", response_model=TrainingResponse)
async def update_training(
    request: Request,
    training_id: UUID,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    video: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin"]))
):
    repository = TrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = UpdateTraining(repository, storage)
    
    training_data = TrainingUpdate(
        title=title,
        description=description
    )
    video_bytes = await video.read() if video and video.filename else None
    image_bytes = await image.read() if image and image.filename else None

    return use_case.execute(
        training_id,
        training_data,
        video_bytes,
        video.filename if video and video.filename else None,
        image_bytes,
        image.filename if image and image.filename else None
    )
    
@training_router.delete("/{training_id}")
def delete_training(
    training_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin"]))
):
    repository = TrainingRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = DeleteTraining(repository, storage)

    return use_case.execute(training_id)