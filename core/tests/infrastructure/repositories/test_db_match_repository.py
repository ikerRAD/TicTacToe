from django.test import TestCase

from core.domain.models.match import Match, MatchStatuses
from core.domain.models.user import User
from core.infrastructure.repositories.db_match_repository import DbMatchRepository


class TestIntegrationDbMatchRepository(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User(username="user1", password="1234")
        cls.user.save()

        cls.guest = User(username="user2", password="1234")
        cls.guest.save()

        cls.guest2 = User(username="user3", password="1234")
        cls.guest2.save()

    def setUp(self) -> None:
        self.db_match_repository = DbMatchRepository()

    def test_save(self) -> None:
        matches: list[Match] = list(Match.objects.all())
        self.assertEqual([], matches)

        self.db_match_repository.save(self.user)

        matches: list[Match] = list(Match.objects.all())
        self.assertEqual(1, len(matches))

        match = matches[0]
        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.AWAITING.value, match.status)
        self.assertIsNone(match.winner)
        self.assertIsNone(match.second_player)
        self.assertEqual(0, match.number_of_movements)

        match.delete()
