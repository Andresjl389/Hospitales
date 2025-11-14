from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.option_port import IOptionRepository


class DeleteOption:
    def __init__(self, repo: IOptionRepository):
        self.repo = repo
        
    def execute(self, option_id: UUID):
        option = self.repo.get_by_id(option_id)
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        
        self.repo.delete(option.id)
        raise HTTPException(status_code=200, detail="Option deleted successfully") 