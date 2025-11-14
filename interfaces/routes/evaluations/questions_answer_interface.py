from typing import Optional
from uuid import UUID
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from application.schemas.evaluations.option_schema import OptionCreate, OptionResponse, OptionUpdate
from application.schemas.evaluations.question_type_schema import QuestionTypeBase
from application.use_cases.evaluations.questions_answers.create_option import CreateOption
from application.use_cases.evaluations.questions_answers.create_question import CreateQuestion
from application.use_cases.evaluations.questions_answers.delete_option import DeleteOption
from application.use_cases.evaluations.questions_answers.delete_question import DeleteQuestion
from application.use_cases.evaluations.questions_answers.get_question import GetQuestion
from application.use_cases.evaluations.questions_answers.list_options import ListOptions
from application.use_cases.evaluations.questions_answers.list_question_types import ListQuestionType
from application.use_cases.evaluations.questions_answers.list_questions import ListQuestions
from application.use_cases.evaluations.questions_answers.update_option import UpdateOption
from application.use_cases.evaluations.questions_answers.update_question import UpdateQuestion
from core.config import get_db
from application.schemas.evaluations.question_schema import QuestionBase, QuestionResponse, QuestionUpdate
from core.security import get_current_user, require_role
from domain.models.users.user import User
from infrastructure.repositories.evaluations.option_repository import OptionRepository
from infrastructure.repositories.evaluations.question_repository import QuestionRepository
from infrastructure.repositories.evaluations.question_type_repository import QuestionTypeRepository



questions_router = APIRouter(
    prefix='/evaluations',
    tags=['Evaluations']
)

@questions_router.post('/questions', response_model=QuestionResponse)
async def create_question(question: QuestionBase, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionRepository(db)
    use_case = CreateQuestion(repo)
    return use_case.execute(question)

@questions_router.get('/questions/{question_id}', response_model=QuestionResponse)
async def get_question(question_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = QuestionRepository(db)
    use_case = GetQuestion(repo)
    return use_case.execute(question_id)

@questions_router.get('/questions', response_model=list[QuestionResponse])
async def list_questions(training_id: Optional[UUID] = None, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = QuestionRepository(db)
    use_case = ListQuestions(repo)
    return use_case.execute(training_id)

@questions_router.put('/questions/{question_id}', response_model=QuestionResponse)
async def update_questions(question: QuestionUpdate, question_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionRepository(db)
    use_case = UpdateQuestion(repo)
    return use_case.execute(question, question_id)

@questions_router.delete('/questions/{question_id}')
async def delete_question(question_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionRepository(db)
    use_case = DeleteQuestion(repo)
    return use_case.execute(question_id)

@questions_router.get('/question_types', response_model=list[QuestionTypeBase])
async def get_question_types(question_id: Optional[UUID] = None, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionTypeRepository(db)
    use_case = ListQuestionType(repo)
    return use_case.execute(question_id)

@questions_router.post('/option', response_model=OptionResponse)
async def create_option(option: OptionCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = OptionRepository(db)
    repo_question = QuestionRepository(db)
    repo_question_type = QuestionTypeRepository(db)
    use_case = CreateOption(repo, repo_question, repo_question_type)
    return use_case.execute(option)

@questions_router.get('/options', response_model=list[OptionResponse])
async def list_options(question_id: Optional[UUID] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = OptionRepository(db)
    use_case = ListOptions(repo)
    return use_case.execute(question_id)

@questions_router.put('/options/{option_id}', response_model=OptionResponse)
async def update_option(option_data: OptionUpdate, option_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = OptionRepository(db)
    repo_question = QuestionRepository(db)
    repo_question_type = QuestionTypeRepository(db)
    use_case = UpdateOption(repo, repo_question, repo_question_type)
    return use_case.execute(option_data, option_id)

@questions_router.delete('/options/{option_id}')
async def delete_option(option_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = OptionRepository(db)
    use_case = DeleteOption(repo)
    return use_case.execute(option_id)