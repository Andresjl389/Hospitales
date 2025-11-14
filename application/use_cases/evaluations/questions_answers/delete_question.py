from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.question_port import IQuestionRepository


class DeleteQuestion:
    def __init__(self, repo: IQuestionRepository):
        self.repo = repo
        
    def execute(self, question_id: UUID):
        question = self.repo.get_by_id(question_id)
        if not question:
            raise HTTPException(status_code=404, detail="question not found")
        self.repo.delete(question.id)
        raise HTTPException(status_code=200, detail="Question deleted successfully") 
        