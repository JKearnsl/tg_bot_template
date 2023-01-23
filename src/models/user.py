from enum import Enum


class UserStatus(int, Enum):
    CONFIRMED = 0
    UNCONFIRMED = 1
    BANNED = 2
