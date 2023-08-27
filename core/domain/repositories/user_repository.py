from abc import ABC, abstractmethod

from core.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, username: str, password: str) -> User:
        pass
