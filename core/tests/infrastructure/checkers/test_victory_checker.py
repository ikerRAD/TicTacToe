from django.test import TestCase

from core.domain.models.match import Match, MatchStatuses
from core.domain.models.movement import Movement
from core.domain.models.user import User
from core.infrastructure.checkers.victory_checker import VictoryChecker
from core.infrastructure.generators.board_generator import BoardGenerator
from core.infrastructure.repositories.db_match_repository import DbMatchRepository


class TestVictoryChecker(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.creator = User(username="user1", password="1234")
        cls.creator.save()

        cls.guest = User(username="user2", password="1234")
        cls.guest.save()

        cls.match_with_winner = Match(
            first_player=cls.creator,
            second_player=cls.guest,
            status=MatchStatuses.IN_PROGRESS,
        )
        cls.match_with_winner.save()

        Movement.objects.create(
            x=0, y=0, player=cls.creator, number=1, match=cls.match_with_winner
        )
        Movement.objects.create(
            x=1, y=1, player=cls.creator, number=2, match=cls.match_with_winner
        )
        Movement.objects.create(
            x=2, y=2, player=cls.creator, number=3, match=cls.match_with_winner
        )

        cls.match_without_winner = Match(
            first_player=cls.creator,
            second_player=cls.guest,
            status=MatchStatuses.IN_PROGRESS,
        )
        cls.match_without_winner.save()

        Movement.objects.create(
            x=0, y=0, player=cls.creator, number=1, match=cls.match_without_winner
        )
        Movement.objects.create(
            x=1, y=1, player=cls.creator, number=2, match=cls.match_without_winner
        )
        Movement.objects.create(
            x=2, y=2, player=cls.guest, number=3, match=cls.match_without_winner
        )

    def setUp(self) -> None:
        self.victory_checker = VictoryChecker(DbMatchRepository(), BoardGenerator())

    def test_check_victory(self) -> None:
        winner = self.victory_checker.check(self.match_with_winner.id)

        self.assertEqual("first player", winner)

    def test_check_no_victory(self) -> None:
        winner = self.victory_checker.check(self.match_without_winner.id)

        self.assertIsNone(winner)
