from models import tables
from services.repository.base import BaseRepository


class MusicRequestRepo(BaseRepository[tables.MusicRequest]):
    table = tables.MusicRequest
