from typing import Optional

from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository


class DbUserRepository(UserRepository):
    __slots__ = "__user_manager"

    def __init__(self):
        self.__user_manager = User.objects

    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            return self.__user_manager.get(id=user_id)
        except User.DoesNotExist:
            return None

    def find_user_by_username(self, username: str) -> Optional[User]:
        try:
            return self.__user_manager.get(username=username)
        except User.DoesNotExist:
            return None

    def save(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        user.save()

        return user
