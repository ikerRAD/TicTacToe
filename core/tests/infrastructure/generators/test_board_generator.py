from unittest import TestCase
from unittest.mock import Mock

from core.domain.models.match import Match
from core.domain.models.movement import Movement
from core.infrastructure.generators.board_generator import BoardGenerator


class TestBoardGenerator(TestCase):
    def setUp(self) -> None:
        self.match = Mock(spec=Match)
        self.board_generator = BoardGenerator()

    def test_generate(self) -> None:
        self.match.movements.all.return_value = [
            Mock(
                spec=Movement,
                x=0,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
            Mock(
                spec=Movement,
                x=1,
                y=1,
                **{"get_which_player.return_value": "second player"}
            ),
            Mock(
                spec=Movement,
                x=1,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
            Mock(
                spec=Movement,
                x=0,
                y=2,
                **{"get_which_player.return_value": "second player"}
            ),
            Mock(
                spec=Movement,
                x=2,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
        ]

        board = self.board_generator.generate(self.match)

        self.assertEqual(
            [
                ["first player", None, "second player"],
                ["first player", "second player", None],
                ["first player", None, None],
            ],
            board,
        )

    def test_generate_game_mode(self) -> None:
        self.match.movements.all.return_value = [
            Mock(
                spec=Movement,
                x=0,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
            Mock(
                spec=Movement,
                x=1,
                y=1,
                **{"get_which_player.return_value": "second player"}
            ),
            Mock(
                spec=Movement,
                x=1,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
            Mock(
                spec=Movement,
                x=0,
                y=2,
                **{"get_which_player.return_value": "second player"}
            ),
            Mock(
                spec=Movement,
                x=2,
                y=0,
                **{"get_which_player.return_value": "first player"}
            ),
        ]

        board = self.board_generator.generate(self.match, True)

        self.assertEqual([["X", None, "O"], ["X", "O", None], ["X", None, None]], board)

    def test_generate_empty(self) -> None:
        self.match.movements.all.return_value = []

        board = self.board_generator.generate(self.match)

        self.assertEqual(
            [[None, None, None], [None, None, None], [None, None, None]], board
        )
