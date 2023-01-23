from typing import Optional

from models.role import UserRole
from models.user import UserStatus
from services.repository import UserRepo


class UserService:

    def __init__(self, user_repo: UserRepo):
        self._user = user_repo

    async def create_user(
            self,
            telegram_id: int,
            *,
            record_book_id: Optional[int] = None,
            status: Optional[int] = UserStatus.UNCONFIRMED,
            role: Optional[str] = UserRole.USER
    ) -> None:
        await self._user.create(
            id=telegram_id,
            role=role,
            **{'record_book_id': record_book_id} if record_book_id else {},
            **{'status': status} if status else {},
        )

    async def get_user(self, telegram_id: int) -> Optional[dict]:
        user = await self._user.get(id=telegram_id)
        return user #user.to_dict() if user else None  # TODO: to_dict() is not a good idea

    async def update_user(
            self,
            telegram_id: int,
            *,
            record_book_id: Optional[int] = None,
            role: Optional[str] = None,
            status: Optional[int] = None
    ) -> None:
        await self._user.update(
            telegram_id,
            **{'record_book_id': record_book_id} if record_book_id else {},
            **{'role': role} if role else {},
            **{'status': status} if status else {},
        )
