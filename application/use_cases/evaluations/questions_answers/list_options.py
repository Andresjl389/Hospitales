from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from application.ports.evaluations.option_port import IOptionRepository


class ListOptions:
    def __init__(self, repo: IOptionRepository):
        self.repo = repo
        
    def execute(self, question_id: Optional[UUID] = None):
        if question_id:
            list_options = self.repo.get_by_id_question(question_id)
        else:
            list_options = self.repo.get_all()
        if not list_options:
            raise HTTPException(status_code=404, detail="Option not found")
        
        return list_options