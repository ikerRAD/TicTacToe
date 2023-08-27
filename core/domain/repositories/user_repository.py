from abc import ABC, abstractmethod
from typing import Optional

from core.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, username: str, password: str) -> User:
        pass
