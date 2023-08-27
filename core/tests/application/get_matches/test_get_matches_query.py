from unittest import TestCase
from unittest.mock import Mock

from core.application.get_matches.get_matches_query import GetMatchesQuery
from core.application.get_matches.get_matches_query_response import (
    GetMatchesQueryResponse,
)
from core.domain.models.match import Match
from core.domain.repositories.match_repository import MatchRepository


class TestGetMatchesQuery(TestCase):
    def setUp(self) -> None:
        self.match_repository = Mock(spec=MatchRepository)
        self.query = GetMatchesQuery(self.match_repository)
        self.match = Mock(spec=Match)

    def test_handle(self) -> None:
        self.match_repository.find_by_user_id.return_value = [self.match]

        retrieved_response = self.query.handle(1)

        self.assertEqual(
            GetMatchesQueryResponse(matches=[self.match]), retrieved_response
        )
        self.match_repository.find_by_user_id.assert_called_once_with(1)
