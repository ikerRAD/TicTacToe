from dataclasses import dataclass

from core.application.query_response import QueryResponse
from core.domain.models.match import Match


@dataclass(frozen=True)
class GetMatchesQueryResponse(QueryResponse):
    matches: list[Match]
