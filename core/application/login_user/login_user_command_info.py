from core.domain.models.user import User


class LoginUserCommandInfo(Exception):
    __slots__ = "user"

    def __init__(self, user: User):
        self.user = user
