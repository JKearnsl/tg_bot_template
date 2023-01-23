from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from services import ServiceFactory


class AuthMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        if not getattr(obj, "from_user", None):
            raise CancelHandler()

        service: ServiceFactory = data.get("service")
        if not service:
            raise RuntimeError("ServiceFactory is not found in data")
        user_service = service.user

        user = await user_service.get_user(obj.from_user.id)
        if not user:
            await user_service.create_user(obj.from_user.id)
            user = await user_service.get_user(obj.from_user.id)
        data["user"] = user

    async def post_process(self, obj, data, *args):
        del data["user"]
