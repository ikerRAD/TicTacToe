from unittest import TestCase
from unittest.mock import Mock

from core.application.make_movement.make_movement_command import MakeMovementCommand
from core.domain.exceptions.last_movement_made_exception import (
    LastMovementMadeException,
)
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository
from core.domain.repositories.movement_repository import MovementRepository
from core.infrastructure.checkers.victory_checker import VictoryChecker


class TestMakeMovementCommand(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = Mock(spec=User)

    def setUp(self) -> None:
        self.movement_repository = Mock(spec=MovementRepository)
        self.victory_checker = Mock(spec=VictoryChecker)
        self.match_repository = Mock(spec=MatchRepository)
        self.command = MakeMovementCommand(
            self.movement_repository, self.victory_checker, self.match_repository
        )

    def test_handle_no_finish(self) -> None:
        self.victory_checker.check.return_value = None

        self.command.handle(1, self.user, 0, 0)

        self.movement_repository.save.assert_called_once_with(1, self.user, 0, 0)
        self.victory_checker.check.assert_called_once_with(1)
        self.match_repository.end_match.assert_not_called()

    def test_handle_winner(self) -> None:
        self.victory_checker.check.return_value = "first player"

        self.command.handle(1, self.user, 0, 0)

        self.movement_repository.save.assert_called_once_with(1, self.user, 0, 0)
        self.victory_checker.check.assert_called_once_with(1)
        self.match_repository.end_match.assert_called_once_with(1, "first player")

    def test_handle_end(self) -> None:
        self.movement_repository.save.side_effect = LastMovementMadeException()
        self.victory_checker.check.return_value = None

        self.command.handle(1, self.user, 0, 0)

        self.movement_repository.save.assert_called_once_with(1, self.user, 0, 0)
        self.victory_checker.check.assert_called_once_with(1)
        self.match_repository.end_match.assert_called_once_with(1, None)
