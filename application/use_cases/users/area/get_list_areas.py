from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository
from domain.models.users.area import Area

class ListAreas:
    def __init__(self, repo: IAreaRepository):
        self.repo = repo

    def execute(self) -> list[Area]:
        areas = self.repo.get_all()
        if not areas:
            raise HTTPException(status_code=404, detail="No areas found")
        return areas