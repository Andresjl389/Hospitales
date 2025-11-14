from uuid import UUID
from fastapi import HTTPException
from application.ports.users.area_port import IAreaRepository
from domain.models.users.area import Area

class GetArea:
    def __init__(self, repo: IAreaRepository):
        self.repo = repo

    def execute(self, area_id: UUID) -> Area | None:
        area = self.repo.get_by_id(area_id)
        if not area:
            raise HTTPException(status_code=404, detail="No areas found")
        return area