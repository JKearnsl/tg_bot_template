from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from services import ServiceFactory


class ServiceMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        repo_factory = data.get("repo")
        if not repo_factory:
            raise RuntimeError("RepoFactory is not found in data")
        data["service"] = ServiceFactory(repo_factory)

    async def post_process(self, obj, data, *args):
        del data["service"]
