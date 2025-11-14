from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.question_port import IQuestionRepository
from application.schemas.evaluations.question_schema import QuestionBase
from domain.models.evaluations.question import Question
from sqlalchemy.orm import Session

class CreateQuestion:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo

    def execute(self, question: QuestionBase) -> Question:
        new_question = Question(
            question_text=question.question_text,
            questionnaire_id=question.questionnaire_id,
            question_type_id=question.question_type_id
        )
        created_question = self.repo.create(new_question)
        if not created_question:
            raise HTTPException(status_code=400, detail="Error creating question")
        return created_question