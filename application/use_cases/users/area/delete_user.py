from uuid import UUID

from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository


class DeleteArea:
    def __init__(self, area_repository: IAreaRepository):
        self.area_repository = area_repository
        
    def execute(self, area_id: UUID):
        user = self.area_repository.get_by_id(area_id)
        if not user:
            raise HTTPException(status_code=404, detail="Area not found")
        self.area_repository.delete(area_id)
        raise HTTPException(status_code=200, detail="Area deleted successfully")