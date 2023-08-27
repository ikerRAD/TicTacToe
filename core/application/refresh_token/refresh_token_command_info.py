from core.domain.models.user import User


class RefreshTokenCommandInfo(Exception):
    __slots__ = "user"

    def __init__(self, user: User):
        self.user = user
