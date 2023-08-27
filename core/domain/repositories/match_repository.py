from abc import ABC, abstractmethod

from core.domain.models.match import Match
from core.domain.models.user import User


class MatchRepository(ABC):
    @abstractmethod
    def save(self, creator: User) -> Match:
        pass