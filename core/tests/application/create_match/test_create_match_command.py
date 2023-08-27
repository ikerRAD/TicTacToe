from unittest import TestCase
from unittest.mock import Mock

from core.application.create_match.create_match_command import CreateMatchCommand
from core.application.create_match.create_match_command_info import (
    CreateMatchCommandInfo,
)
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class TestCreateMatchCommand(TestCase):
    def setUp(self) -> None:
        self.match_repository = Mock(spec=MatchRepository)
        self.command = CreateMatchCommand(self.match_repository)
        self.user = Mock(spec=User)

    def test_handle(self) -> None:
        with self.assertRaises(CreateMatchCommandInfo):
            self.command.handle(self.user)

        self.match_repository.save.assert_called_once_with(self.user)
