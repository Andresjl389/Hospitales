from datetime import date, datetime, timezone
from uuid import UUID
from application.ports.evaluations.option_port import IOptionRepository
from application.ports.evaluations.question_port import IQuestionRepository
from application.ports.evaluations.user_answer_port import IUserAnswerRepository
from application.schemas.evaluations.user_answer_schema import UserAnswerCreate
from fastapi import HTTPException

from domain.models.evaluations.user_answer import UserAnswer


class CreateUserAnswer:
    def __init__(
        self, repo: IUserAnswerRepository,
        repo_question: IQuestionRepository,
        repo_option = IOptionRepository
    ):
        self.repo = repo
        self.repo_option = repo_option
        self.repo_question = repo_question
    def execute(self, user_id: UUID, user_answer: UserAnswerCreate):
        if not user_id:
            raise HTTPException(status_code=404, detail="User id is required")
        
        question = self.repo_question.get_by_id(user_answer.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        option = self.repo_option.get_by_id(user_answer.option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        
        new_user_answer = UserAnswer(
            answer_date = date.today(),
            user_id = user_id,
            question_id = user_answer.question_id,
            option_id = user_answer.option_id
        )
        
        self.repo.create(new_user_answer)
        return new_user_answer