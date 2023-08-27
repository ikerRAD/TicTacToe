from unittest import TestCase
from unittest.mock import Mock

from core.application.get_match.get_match_query import GetMatchQuery
from core.application.get_match.get_match_query_response import GetMatchQueryResponse
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.models.match import Match
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository
from core.infrastructure.generators.board_generator import BoardGenerator


class TestGetMatchQuery(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.match = Mock(spec=Match)
        cls.user = Mock(spec=User, id=1)

    def setUp(self) -> None:
        self.match_repository = Mock(spec=MatchRepository)
        self.board_generator = Mock(spec=BoardGenerator)
        self.query = GetMatchQuery(self.match_repository, self.board_generator)

    def test_handle(self) -> None:
        self.match.first_player_id = 1
        self.match_repository.find_or_fail_by_id.return_value = self.match
        self.board_generator.generate.return_value = []
        expected_response = GetMatchQueryResponse(
            status=self.match.status,
            number_of_movements=self.match.number_of_movements,
            board=[],
            first_player=self.match.first_player,
            second_player=self.match.second_player,
            winner=self.match.get_which_player_wins.return_value,
        )

        retrieved_response = self.query.handle(10, self.user)

        self.assertEqual(expected_response, retrieved_response)
        self.match_repository.find_or_fail_by_id.assert_called_once_with(10)
        self.board_generator.generate.assert_called_once_with(self.match, True)

    def test_handle_foreign_user(self) -> None:
        self.match.first_player_id = 2
        self.match.second_player_id = 3
        self.match_repository.find_or_fail_by_id.return_value = self.match

        with self.assertRaises(NotInGameException):
            self.query.handle(10, self.user)

        self.match_repository.find_or_fail_by_id.assert_called_once_with(10)
        self.board_generator.generate.assert_not_called()
