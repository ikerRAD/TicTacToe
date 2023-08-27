from core.domain.models.match import Match
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class DbMatchRepository(MatchRepository):
    def save(self, creator: User) -> Match:
        match = Match(first_player=creator)
        match.save()

        creator.matches_total = creator.matches_total + 1
        creator.save()

        return match
