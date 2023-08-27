from django.contrib.auth.models import User

from core.application.get_match.get_match_query_response import GetMatchQueryResponse
from core.application.query import Query
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.repositories.match_repository import MatchRepository
from core.infrastructure.generators.board_generator import BoardGenerator


class GetMatchQuery(Query):
    __slots__ = ("__match_repository", "__board_generator")

    def __init__(
        self, match_repository: MatchRepository, board_generator: BoardGenerator
    ):
        self.__match_repository = match_repository
        self.__board_generator = board_generator

    def handle(self, match_id: int, user: User) -> GetMatchQueryResponse:
        match = self.__match_repository.find_or_fail_by_id(match_id)

        is_user_in_match = (
            match.first_player_id == user.id or match.second_player_id == user.id
        )
        if is_user_in_match is False:
            raise NotInGameException()

        game_board = self.__board_generator.generate(match, True)

        return GetMatchQueryResponse(
            status=match.status,
            number_of_movements=match.number_of_movements,
            board=game_board,
            first_player=match.first_player,
            second_player=match.second_player,
            winner=match.get_which_player_wins(),
        )
