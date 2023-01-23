import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types.base import TelegramObject

from models.user import UserStatus


class UserStatusFilter(BoundFilter):
    key = 'user_status'

    def __init__(
        self,
        user_status: typing.Union[None, UserStatus, typing.Collection[UserStatus]] = None,
    ):
        if user_status is None:
            self.user_status = None
        elif isinstance(user_status, UserStatus):
            self.user_status = {user_status}
        else:
            self.user_status = set(user_status)

    async def check(self, obj: TelegramObject):
        if self.user_status is None:
            return True
        data = ctx_data.get()
        user = data.get("user")
        return user.status in self.user_status


class BannedFilter(BoundFilter):
    key = 'is_banned'

    def __init__(self, is_banned: typing.Optional[bool] = None):
        self.is_banned = is_banned

    async def check(self, obj: TelegramObject):
        if self.is_banned is None:
            return True
        data = ctx_data.get()
        user = data.get("user")
        return (user.status is UserStatus.BANNED) == self.is_banned


class UnconfirmedFilter(BoundFilter):
    key = 'is_unconfirmed'

    def __init__(self, is_unconfirmed: typing.Optional[bool] = None):
        self.is_unconfirmed = is_unconfirmed

    async def check(self, obj: TelegramObject):
        if self.is_unconfirmed is None:
            return True
        data = ctx_data.get()
        user = data.get("user")
        return (user.status is UserStatus.UNCONFIRMED) == self.is_unconfirmed
