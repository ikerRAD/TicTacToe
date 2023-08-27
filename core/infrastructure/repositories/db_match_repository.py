from core.domain.exceptions.match_not_accepting_guests_exception import (
    MatchNotAcceptingGuestsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.repeated_player_exception import RepeatedPlayerException
from core.domain.models.match import Match, MatchStatuses
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class DbMatchRepository(MatchRepository):
    __slots__ = "__match_manager"

    def __init__(self):
        self.__match_manager = Match.objects

    def save(self, creator: User) -> Match:
        match = Match(first_player=creator)
        match.save()

        creator.matches_total = creator.matches_total + 1
        creator.save()

        return match

    def save_guest(self, guest: User, match_id: int) -> None:
        try:
            match = self.__match_manager.get(id=match_id)
        except Match.DoesNotExist:
            raise MatchNotFoundException()

        if match.status != MatchStatuses.AWAITING.value:
            raise MatchNotAcceptingGuestsException()

        if match.first_player_id == guest.id:
            raise RepeatedPlayerException()

        match.second_player = guest
        match.status = MatchStatuses.IN_PROGRESS
        match.save()

        guest.matches_total = guest.matches_total + 1
        guest.save()
