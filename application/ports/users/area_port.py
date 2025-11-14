from application.ports.base_repository import IBaseRepository
from domain.models.users.area import Area
from typing import Optional

class IAreaRepository(IBaseRepository[Area]):
    def get_by_name(self, name: str) -> Optional[Area]: ...