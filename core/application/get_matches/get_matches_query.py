from core.application.get_matches.get_matches_query_response import (
    GetMatchesQueryResponse,
)
from core.application.query import Query
from core.domain.repositories.match_repository import MatchRepository


class GetMatchesQuery(Query):
    __slots__ = "__match_repository"

    def __init__(self, match_repository: MatchRepository):
        self.__match_repository = match_repository

    def handle(self, user_id: int) -> GetMatchesQueryResponse:
        matches = self.__match_repository.find_by_user_id(user_id)

        return GetMatchesQueryResponse(matches)
