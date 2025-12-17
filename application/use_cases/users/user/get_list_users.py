from application.ports.users.user_port import IUserRepository
from domain.models.users.user import User

class ListUsers:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self) -> list[User]:
        users = self.repo.get_all()
        # Return an empty list when there are no users instead of raising a 404.
        # This allows clients (like the admin dashboard) to render zero counts gracefully
        # when the database is freshly created.
        return users or []
