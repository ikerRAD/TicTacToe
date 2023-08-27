from abc import ABC, abstractmethod

from core.domain.models.user import User


class MovementRepository(ABC):
    @abstractmethod
    def save(self, match_id: int, player: User, x: int, y: int) -> None:
        pass
