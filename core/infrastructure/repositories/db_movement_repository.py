from core.domain.exceptions.illegal_movement_exception import IllegalMovementException
from core.domain.exceptions.invalid_turn_exception import InvalidTurnException
from core.domain.exceptions.last_movement_made_exception import (
    LastMovementMadeException,
)
from core.domain.exceptions.match_not_accepting_movements_exception import (
    MatchNotAcceptingMovementsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.maximum_number_of_movements_exceeded_exception import (
    MaximumNumberOfMovementsExceededException,
)
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.exceptions.repeated_movement_exception import RepeatedMovementException
from core.domain.models.match import Match, MatchPlayer, MatchStatuses
from core.domain.models.movement import Movement
from core.domain.models.user import User
from core.domain.repositories.movement_repository import MovementRepository


class DbMovementRepository(MovementRepository):
    __slots__ = ("__match_manager", "__movement_manager")

    def __init__(self):
        self.__match_manager = Match.objects
        self.__movement_manager = Movement.objects

    def save(self, match_id: int, player: User, x: int, y: int) -> None:
        try:
            match = self.__match_manager.get(id=match_id)
        except Match.DoesNotExist:
            raise MatchNotFoundException()

        if match.status != MatchStatuses.IN_PROGRESS.value:
            raise MatchNotAcceptingMovementsException()

        is_match_player = (
            match.first_player_id == player.id or match.second_player_id == player.id
        )
        if not is_match_player:
            raise NotInGameException()

        turn = match.turn
        if turn == MatchPlayer.FIRST_PLAYER.value:
            self.__validate_is_first_player(match, player)
        elif turn == MatchPlayer.SECOND_PLAYER.value:
            self.__validate_is_second_player(match, player)

        movement_number = match.number_of_movements + 1
        if movement_number > 9:
            raise MaximumNumberOfMovementsExceededException()

        if x < 0 or x > 2 or y < 0 or y > 2:
            raise IllegalMovementException()

        try:
            self.__movement_manager.get(x=x, y=y, match=match)
            raise RepeatedMovementException()
        except Movement.DoesNotExist:
            pass

        movement = Movement(
            x=x, y=y, match=match, player=player, number=movement_number
        )
        movement.save()

        match.number_of_movements = match.number_of_movements + 1
        match.save()

        if movement_number == 9:
            raise LastMovementMadeException()

    def __validate_is_first_player(self, match: Match, player: User) -> None:
        if match.first_player_id != player.id:
            raise InvalidTurnException()

    def __validate_is_second_player(self, match: Match, player: User) -> None:
        if match.second_player_id != player.id:
            raise InvalidTurnException()
