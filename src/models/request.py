from enum import Enum


class RequestStatus(int, Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
