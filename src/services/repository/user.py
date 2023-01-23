from models import tables
from services.repository.base import BaseRepository


class UserRepo(BaseRepository[tables.User]):
    table = tables.User
