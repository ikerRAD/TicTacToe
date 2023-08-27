from abc import ABC, abstractmethod
from typing import Optional

from core.domain.models.match import Match
from core.domain.models.user import User


class MatchRepository(ABC):
    @abstractmethod
    def find_or_fail_by_id(self, match_id: int) -> Match:
        pass

    @abstractmethod
    def save(self, creator: User) -> Match:
        pass

    @abstractmethod
    def save_guest(self, guest: User, match_id: int) -> None:
        pass

    @abstractmethod
    def end_match(self, match_id: int, winner: Optional[str]) -> None:
        pass
