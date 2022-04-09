from enum import Enum, auto


class RoleType(Enum):
    ADMIN = auto()
    MEMBER = auto()


class EmailStatus(Enum):
    EMAIL_EXISTS = True
    EMAIL_DOES_NOT_EXIST = False
