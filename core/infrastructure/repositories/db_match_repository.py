from typing import Optional
from django.db.models import Q

from core.domain.exceptions.match_not_accepting_guests_exception import (
    MatchNotAcceptingGuestsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.repeated_player_exception import RepeatedPlayerException
from core.domain.models.match import Match, MatchStatuses, MatchPlayer
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class DbMatchRepository(MatchRepository):
    __slots__ = "__match_manager"

    def __init__(self):
        self.__match_manager = Match.objects

    def find_by_user_id(self, user_id: int) -> list[Match]:
        first_player_query = Q(first_player_id=user_id)
        second_player_query = Q(second_player_id=user_id)

        return self.__match_manager.filter(first_player_query | second_player_query)

    def find_or_fail_by_id(self, match_id: int) -> Match:
        try:
            return self.__match_manager.get(id=match_id)
        except Match.DoesNotExist:
            raise MatchNotFoundException()

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

    def end_match(self, match_id: int, winner: Optional[str]) -> None:
        try:
            match = self.__match_manager.get(id=match_id)
        except Match.DoesNotExist:
            raise MatchNotFoundException()

        match.status = MatchStatuses.FINISHED
        match.set_which_player_wins(winner)
        match.save()

        if winner is not None:
            if winner == MatchPlayer.FIRST_PLAYER.value:
                winner_player = match.first_player
                winner_player.matches_won = winner_player.matches_won + 1
                winner_player.save()
            elif winner == MatchPlayer.SECOND_PLAYER.value:
                winner_player = match.second_player
                winner_player.matches_won = winner_player.matches_won + 1
                winner_player.save()
