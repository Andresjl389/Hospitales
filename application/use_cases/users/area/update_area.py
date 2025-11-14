from uuid import UUID
from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository
from application.schemas.users.area_schema import CreateAreaSchema
from domain.models.users.area import Area

class UpdateArea:
    def __init__(self, repo: IAreaRepository):
        self.repo = repo
    def execute(self, area_id: UUID, area: CreateAreaSchema) -> Area | None:
        existing_area = self.repo.get_by_id(area_id)
        if not existing_area:
            raise HTTPException(status_code=404, detail="Area not found")
        existing_area.name = area.name
        updated_area = self.repo.update(existing_area)
        if not updated_area:
            raise HTTPException(status_code=400, detail="Error updating area")
        return updated_area