from application.ports.users.role_port import IRoleRepository
from domain.models.users.role import Role


class ListRoles:
    def __init__(self, repo: IRoleRepository):
        self.repo = repo

    def execute(self) -> list[Role]:
        roles = self.repo.get_all()
        return roles or []
