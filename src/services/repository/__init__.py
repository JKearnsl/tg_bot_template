from .user import UserRepo
from .request import MusicRequestRepo


class RepoFactory:
    def __init__(self, session):
        self._session = session

    def user(self) -> UserRepo:
        return UserRepo(self._session)

    def request(self) -> MusicRequestRepo:
        return MusicRequestRepo(self._session)
