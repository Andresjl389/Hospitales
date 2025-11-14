from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from application.schemas.trainings.assignment_schema import AssignmentBase, AssignmentResponse, AssignmentUpdate
from application.use_cases.trainings.assignment.change_assignment import UpdateAssignment
from application.use_cases.trainings.assignment.create_assignment import CreateAssignment
from application.use_cases.trainings.assignment.delete_assignment import DeleteAssignment
from application.use_cases.trainings.assignment.get_assignment import GetAssignment
from application.use_cases.trainings.assignment.list_assignments import ListAssignments
from application.use_cases.trainings.user_training.create_user_training import CreateUserTraining
from core.config import get_db
from core.security import require_role, get_current_user
from domain.models.users.user import User
from infrastructure.repositories.trainings.assignment_repository import AssignmentRepository
from infrastructure.repositories.trainings.status_repository import StatusRepository
from infrastructure.repositories.trainings.user_training_repository import UserTrainingRepository
from infrastructure.repositories.users.area_repository import AreaRepository
from infrastructure.repositories.users.user_repository import UserRepository
from infrastructure.storage.filesystem_storage import FileSystemStorageAdapter


assignment_router = APIRouter(
    prefix='/assignments',
    tags=['Assignments']
)

@assignment_router.post('', response_model=AssignmentResponse)
async def create_assignment(
    assignment: AssignmentBase, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_role(["Admin"]))
):
    repo = AssignmentRepository(db)
    status_repo = StatusRepository(db)
    use_case_assignment = CreateAssignment(repo, status_repo)
    
    created_assignment = use_case_assignment.execute(assignment)
    user_training_repo = UserTrainingRepository(db)
    area_repo = AreaRepository(db)
    user_repo = UserRepository(db)
    use_case_user_training = CreateUserTraining(
        user_training_repo, 
        status_repo, 
        area_repo, 
        repo, 
        user_repo
    )
    user_trainings_result = use_case_user_training.execute(created_assignment.id)
    
    return created_assignment

@assignment_router.get('', response_model=list[AssignmentResponse])
async def get_list_assignments(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AssignmentRepository(db)
    use_case = ListAssignments(repo)
    return use_case.execute()

@assignment_router.get('/{area_id}', response_model=list[AssignmentResponse])
async def get_assignments_by_area(area_id: UUID, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = AssignmentRepository(db)
    storage = FileSystemStorageAdapter()
    use_case = GetAssignment(repo, storage, request)
    return use_case.execute(area_id)

@assignment_router.put('/{assignment_id}', response_model=AssignmentResponse)
async def update_assignment(assignment_id: UUID, assignment: AssignmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AssignmentRepository(db)
    status_repo = StatusRepository(db)
    use_case = UpdateAssignment(repo, status_repo)
    return use_case.execute(assignment_id, assignment)

@assignment_router.delete('/{assignment_id}')
async def delete_assignment(assignment_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = AssignmentRepository(db)
    use_case = DeleteAssignment(repo)
    return use_case.execute(assignment_id)
    