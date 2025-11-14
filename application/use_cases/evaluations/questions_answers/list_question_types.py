from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from application.ports.evaluations.question_type_repository import IQuestionTypeRepository
from domain.models.evaluations.question_type import QuestionType


class ListQuestionType:
    def __init__(self, repo: IQuestionTypeRepository):
        self.repo = repo
        
    def execute(self, question_type_id: Optional[UUID] = None) -> list[QuestionType]:
        if question_type_id:
            question_type = self.repo.get_by_id(question_type_id)
            if not question_type:
                raise HTTPException(status_code=404, detail="Question type not found")
            return [question_type]
        
        question_types = self.repo.get_all()
        if not question_types:
            raise HTTPException(status_code=404, detail="No question types found")
        return question_types

        
        