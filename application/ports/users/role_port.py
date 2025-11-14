from application.ports.base_repository import IBaseRepository
from domain.models.users.refresh_token import RefreshToken
from domain.models.users.role import Role
from domain.models.users.user import User
from typing import Optional

class IRoleRepository(IBaseRepository[Role]):
    def get_by_name(self, name: str) -> Optional[Role]: ...