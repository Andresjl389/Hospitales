from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.question_port import IQuestionRepository
from application.schemas.evaluations.question_schema import QuestionBase
from domain.models.evaluations.question import Question

class ListQuestions:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    def execute(self, training_id: Optional[UUID] = None) -> list[Question]:
        if training_id:
            questions = self.repo.get_by_training_id(training_id)
        else:
            questions = self.repo.get_all()
        if not questions:
            raise HTTPException(status_code=404, detail="Question not found")
        return questions