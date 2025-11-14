from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.question_port import IQuestionRepository
from application.schemas.evaluations.question_schema import QuestionBase
from domain.models.evaluations.question import Question
from sqlalchemy.orm import Session

class GetQuestion:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    def execute(self, question_id: UUID) -> Question:
        question = self.repo.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question