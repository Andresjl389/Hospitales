from application.ports.base_repository import IBaseRepository
from typing import Optional

from domain.models.users.refresh_token import RefreshToken

class IRefreshTokenRepository(IBaseRepository[RefreshToken]):
    def delete_by_user_id(self, user_id: str) -> None: ...