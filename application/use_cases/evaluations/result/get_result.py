from uuid import UUID
from fastapi import HTTPException
from application.ports.evaluations.result_port import IResultRepository

class GetResult:
    def __init__(self, repo_result: IResultRepository):
        self.repo_result = repo_result

    def execute(self, result_id: UUID):
        result = self.repo_result.get_by_id(result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return result
