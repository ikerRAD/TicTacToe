from typing import Optional

from core.domain.models.match import Match, MatchPlayer


class BoardGenerator:
    def generate(
        self, match: Match, game_mode: bool = False
    ) -> list[list[Optional[str]]]:
        board: list[list[Optional[str]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        for movement in match.movements.all():
            x: int = movement.x
            y: int = movement.y

            board[x][y] = movement.get_which_player()

        if game_mode is False:
            return board

        return [
            [self.__substitute_to_game_mode(slot) for slot in line] for line in board
        ]

    def __substitute_to_game_mode(self, slot: Optional[str]) -> Optional[str]:
        if slot == MatchPlayer.FIRST_PLAYER.value:
            return "X"
        elif slot == MatchPlayer.SECOND_PLAYER.value:
            return "O"
