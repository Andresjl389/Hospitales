from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from application.schemas.evaluations.questionaire_schema import QuestionnaireBase, QuestionnaireResponse
from application.use_cases.evaluations.questionnaire.create_questionnaire import CreateQuestionnaire
from application.use_cases.evaluations.questionnaire.delete_questionnaire import DeleteQuestionnaire
from application.use_cases.evaluations.questionnaire.get_questionnaire import GetQuestionnaire
from application.use_cases.evaluations.questionnaire.list_questionnaire import ListQuestionnaires
from application.use_cases.evaluations.questionnaire.update_questionnaire import UpdateQuestionnaire
from core.config import get_db
from core.security import require_role
from domain.models.users.user import User
from infrastructure.repositories.evaluations.questionaire_repository import QuestionnaireRepository


questionnaire_router = APIRouter(
    prefix='/questionnaires',
    tags=['Questionnaires']
)

@questionnaire_router.post('', response_model=QuestionnaireResponse)
async def create_questionnaire(questionnaire: QuestionnaireBase, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionnaireRepository(db)
    use_case = CreateQuestionnaire(repo)
    return use_case.execute(questionnaire)

@questionnaire_router.get('/{questionnaire_id}', response_model=QuestionnaireResponse)
async def get_questionnaire(questionnaire_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = QuestionnaireRepository(db)
    use_case = GetQuestionnaire(repo)
    return use_case.execute(questionnaire_id)

@questionnaire_router.get('', response_model=list[QuestionnaireResponse])
async def list_questionnaires(db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = QuestionnaireRepository(db)
    use_case = ListQuestionnaires(repo)
    return use_case.execute()

@questionnaire_router.put('/{questionnaire_id}', response_model=QuestionnaireResponse)
async def update_questionnaire(questionnaire_id: str, questionnaire: QuestionnaireBase, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin", "User"]))):
    repo = QuestionnaireRepository(db)
    use_case = UpdateQuestionnaire(repo)
    return use_case.execute(questionnaire_id, questionnaire)

@questionnaire_router.delete('/{questionnaire_id}')
async def delete_questionnaire(questionnaire_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role(["Admin"]))):
    repo = QuestionnaireRepository(db)
    use_case = DeleteQuestionnaire(repo)
    return use_case.execute(questionnaire_id)
