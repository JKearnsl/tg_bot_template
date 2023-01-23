from . import repository
from .user import UserService


class ServiceFactory:
    def __init__(self, repo_factory: repository.RepoFactory):
        self._repo = repo_factory

    @property
    def user(self) -> UserService:
        return UserService(self._repo.user())
