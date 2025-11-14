from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.schemas.evaluations.result_schema import ResultResponse
from application.schemas.evaluations.user_answer_schema import UserAnswerCreate, UserAnswerResponse
from application.use_cases.evaluations.result.create_result import CreateResult
from application.use_cases.evaluations.result.get_result import GetResult
from application.use_cases.evaluations.result.get_user_answers_by_result import GetUserAnswersByResult
from application.use_cases.evaluations.user_response.create_user_response import CreateUserAnswer
from application.use_cases.evaluations.user_response.get_user_answer import GetUserAnswer
from application.use_cases.evaluations.user_response.upsert_user_answer import UpsertUserAnswer
from core.config import get_db
from core.security import require_role
from domain.models.users.user import User
from infrastructure.repositories.evaluations.answer_repository import UserAnswerRepository
from infrastructure.repositories.evaluations.option_repository import OptionRepository
from infrastructure.repositories.evaluations.question_repository import QuestionRepository
from infrastructure.repositories.evaluations.questionaire_repository import QuestionnaireRepository
from infrastructure.repositories.evaluations.result_repository import ResultRepository
from infrastructure.repositories.trainings.training_repository import TrainingRepository

result_router = APIRouter(
    prefix="/results",
    tags=["Results"]
)


@result_router.post("/user_answer")
async def save_answer(
    user_answer: UserAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    """
    Guarda una nueva respuesta de usuario (solo se usa la primera vez)
    """
    repo = UserAnswerRepository(db)
    repo_question = QuestionRepository(db)
    repo_option = OptionRepository(db)
    use_case = CreateUserAnswer(repo, repo_question, repo_option)
    return use_case.execute(current_user.id, user_answer)


@result_router.put("/user_answer")
async def update_or_resume_exam(
    user_answer: UserAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    """
    Actualiza una respuesta existente o la sobrescribe (para reintentos)
    Soporta tanto respuestas únicas como selección múltiple
    """
    repo_answer = UserAnswerRepository(db)
    repo_question = QuestionRepository(db)
    repo_option = OptionRepository(db)
    use_case = UpsertUserAnswer(repo_answer, repo_question, repo_option)
    
    result = use_case.execute(current_user.id, user_answer)
    
    # Normalizar la respuesta (puede ser una respuesta o lista de respuestas)
    if isinstance(result, list):
        return {"answers": result, "count": len(result)}
    else:
        return result

@result_router.get("/user_answer/{training_id}", response_model=list[UserAnswerResponse])
async def get_user_answer(
    training_id: UUID,
    user_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    """
    Obtiene todas las respuestas del usuario para una capacitación específica
    """
    repo = UserAnswerRepository(db)
    repo_training = TrainingRepository(db)
    use_case = GetUserAnswer(repo, repo_training)
    user = user_id if user_id else current_user.id
    return use_case.execute(training_id, user)


@result_router.post("/{questionnaire_id}", response_model=ResultResponse)
async def create_result(
    questionnaire_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    """
    Calcula y crea un resultado a partir de las respuestas actuales
    """
    repo_result = ResultRepository(db)
    repo_answer = UserAnswerRepository(db)
    repo_questionnaire = QuestionnaireRepository(db)
    use_case = CreateResult(repo_result, repo_answer, repo_questionnaire)
    return use_case.execute(current_user.id, questionnaire_id)


@result_router.get("/{result_id}", response_model=ResultResponse)
async def get_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    repo = ResultRepository(db)
    use_case = GetResult(repo)
    return use_case.execute(result_id)


@result_router.get("/{result_id}/answers", response_model=list[UserAnswerResponse])
async def get_answers_by_result(
    result_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "User"]))
):
    repo_answer = UserAnswerRepository(db)
    repo_result = ResultRepository(db)
    use_case = GetUserAnswersByResult(repo_answer, repo_result)
    return use_case.execute(result_id, current_user)
