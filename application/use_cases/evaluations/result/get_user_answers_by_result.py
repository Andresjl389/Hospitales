from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.result_port import IResultRepository
from application.ports.evaluations.user_answer_port import IUserAnswerRepository
from domain.models.users.user import User


class GetUserAnswersByResult:
    def __init__(self, repo_user_answer: IUserAnswerRepository, repo_result: IResultRepository):
        self.repo_user_answer = repo_user_answer
        self.repo_result = repo_result

    def execute(self, result_id: UUID, current_user: User):
        result = self.repo_result.get_by_id(result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")

        # Usamos la relación indirecta (por cuestionario)
        answers = self.repo_user_answer.get_by_user_and_questionnaire(
            result.user_id, result.questionnaire_id
        )

        if not answers:
            raise HTTPException(status_code=404, detail="No answers found for this result")

        return answers

