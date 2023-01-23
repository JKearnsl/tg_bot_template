from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from services.repository import RepoFactory


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            raise CancelHandler()

        active_session = await self.session().__aenter__()
        data["db"] = active_session
        data["repo"] = RepoFactory(active_session)

    async def post_process(self, obj, data, *args):
        del data["repo"]
        active_session = data.get("db")
        if active_session:
            await self.session().__aexit__(None, None, None)
