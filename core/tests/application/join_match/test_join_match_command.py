from unittest import TestCase
from unittest.mock import Mock

from core.application.join_match.join_match_command import JoinMatchCommand
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class TestJoinMatchCommand(TestCase):
    def setUp(self) -> None:
        self.match_repository = Mock(spec=MatchRepository)
        self.command = JoinMatchCommand(self.match_repository)
        self.guest = Mock(spec=User)

    def test_handle(self) -> None:
        self.command.handle(self.guest, 1)

        self.match_repository.save_guest.assert_called_once_with(self.guest, 1)
