from core.application.command import Command
from core.domain.exceptions.last_movement_made_exception import (
    LastMovementMadeException,
)
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository
from core.domain.repositories.movement_repository import MovementRepository
from core.infrastructure.checkers.victory_checker import VictoryChecker


class MakeMovementCommand(Command):
    __slots__ = ("__movement_repository", "__victory_checker", "__match_repository")

    def __init__(
        self,
        movement_repository: MovementRepository,
        victory_checker: VictoryChecker,
        match_repository: MatchRepository,
    ):
        self.__movement_repository = movement_repository
        self.__victory_checker = victory_checker
        self.__match_repository = match_repository

    def handle(self, match_id: int, player: User, x: int, y: int) -> None:
        is_last = False
        try:
            self.__movement_repository.save(match_id, player, x, y)
        except LastMovementMadeException:
            is_last = True

        winner = self.__victory_checker.check(match_id)

        if is_last is True or winner is not None:
            self.__match_repository.end_match(match_id, winner)
