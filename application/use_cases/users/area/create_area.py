from uuid import UUID
from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository
from application.schemas.users.area_schema import CreateAreaSchema
from domain.models.users.area import Area

class CreateArea:
    def __init__(self, repo: IAreaRepository):
        self.repo = repo

    def execute(self, area: CreateAreaSchema) -> Area:
        new_area = Area(name=area.name)
        created_area = self.repo.create(new_area)
        if not created_area:
            raise HTTPException(status_code=400, detail="Error creating area")
        return created_area