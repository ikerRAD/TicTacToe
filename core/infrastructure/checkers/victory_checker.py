from typing import Optional

from core.domain.models.match import MatchPlayer
from core.domain.repositories.match_repository import MatchRepository
from core.infrastructure.generators.board_generator import BoardGenerator


class VictoryChecker:
    WIN_PATTERNS = [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
    ]
    __slots__ = ("__match_repository", "__board_generator")

    def __init__(
        self, match_repository: MatchRepository, board_generator: BoardGenerator
    ):
        self.__match_repository = match_repository
        self.__board_generator = board_generator

    def check(self, match_id: int) -> Optional[str]:
        match = self.__match_repository.find_or_fail_by_id(match_id)

        board = self.__board_generator.generate(match)

        for position_1, position_2, position_3 in self.WIN_PATTERNS:
            x_1, y_1 = position_1
            x_2, y_2 = position_2
            x_3, y_3 = position_3

            slots = [board[x_1][y_1], board[x_2][y_2], board[x_3][y_3]]

            if (
                all(map(lambda slot: slot == MatchPlayer.FIRST_PLAYER.value, slots))
                is True
            ):
                return MatchPlayer.FIRST_PLAYER.value
            elif (
                all(map(lambda slot: slot == MatchPlayer.SECOND_PLAYER.value, slots))
                is True
            ):
                return MatchPlayer.SECOND_PLAYER.value
