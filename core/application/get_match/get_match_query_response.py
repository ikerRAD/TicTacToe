from dataclasses import dataclass
from typing import Optional

from core.application.query_response import QueryResponse
from core.domain.models.user import User


@dataclass(frozen=True)
class GetMatchQueryResponse(QueryResponse):
    status: str
    number_of_movements: int
    board: list[list[Optional[str]]]
    first_player: User
    second_player: Optional[User]
    winner: Optional[str]
