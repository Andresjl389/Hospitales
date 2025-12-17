from application.ports.users.area_port import IAreaRepository
from domain.models.users.area import Area

class ListAreas:
    def __init__(self, repo: IAreaRepository):
        self.repo = repo

    def execute(self) -> list[Area]:
        areas = self.repo.get_all()
        # Return an empty list when there are no areas so clients can handle
        # the "no data" state without errors.
        return areas or []
