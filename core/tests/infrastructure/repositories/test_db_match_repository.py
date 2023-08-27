from django.test import TestCase
from core.domain.exceptions.match_not_accepting_guests_exception import (
    MatchNotAcceptingGuestsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.repeated_player_exception import RepeatedPlayerException
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

    def test_save_guest(self) -> None:
        match = Match(first_player=self.user)
        match.save()

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.AWAITING.value, match.status)
        self.assertIsNone(match.winner)
        self.assertIsNone(match.second_player)
        self.assertEqual(0, match.number_of_movements)

        self.db_match_repository.save_guest(self.guest, match.id)

        match = Match.objects.get(id=match.id)

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.IN_PROGRESS.value, match.status)
        self.assertIsNone(match.winner)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(0, match.number_of_movements)

        match.delete()

    def test_save_guest_no_match(self) -> None:
        with self.assertRaises(MatchNotFoundException):
            self.db_match_repository.save_guest(self.guest, 0)

    def test_save_guest_match_completed(self) -> None:
        match = Match(first_player=self.user)
        match.save()

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.AWAITING.value, match.status)
        self.assertIsNone(match.winner)
        self.assertIsNone(match.second_player)
        self.assertEqual(0, match.number_of_movements)

        self.db_match_repository.save_guest(self.guest, match.id)

        match = Match.objects.get(id=match.id)

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.IN_PROGRESS.value, match.status)
        self.assertIsNone(match.winner)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(0, match.number_of_movements)

        with self.assertRaises(MatchNotAcceptingGuestsException):
            self.db_match_repository.save_guest(self.guest2, match.id)

        match.delete()

    def test_save_guest_is_creator(self) -> None:
        match = Match(first_player=self.user)
        match.save()

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(MatchStatuses.AWAITING.value, match.status)
        self.assertIsNone(match.winner)
        self.assertIsNone(match.second_player)
        self.assertEqual(0, match.number_of_movements)

        with self.assertRaises(RepeatedPlayerException):
            self.db_match_repository.save_guest(self.user, match.id)

        match.delete()

    def test_end_match_with_winner(self) -> None:
        match = Match(
            first_player=self.user,
            second_player=self.guest,
            status=MatchStatuses.IN_PROGRESS,
        )
        match.save()

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(MatchStatuses.IN_PROGRESS.value, match.status)
        self.assertIsNone(match.winner)

        self.db_match_repository.end_match(match.id, "first player")

        match = Match.objects.get(id=match.id)

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(MatchStatuses.FINISHED.value, match.status)
        self.assertEqual(self.user, match.winner)

        match.delete()

    def test_end_match_without_winner(self) -> None:
        match = Match(
            first_player=self.user,
            second_player=self.guest,
            status=MatchStatuses.IN_PROGRESS,
        )
        match.save()

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(MatchStatuses.IN_PROGRESS.value, match.status)
        self.assertIsNone(match.winner)

        self.db_match_repository.end_match(match.id, None)

        match = Match.objects.get(id=match.id)

        self.assertEqual(self.user, match.first_player)
        self.assertEqual(self.guest, match.second_player)
        self.assertEqual(MatchStatuses.FINISHED.value, match.status)
        self.assertIsNone(match.winner)

        match.delete()

    def test_end_match_no_match(self) -> None:
        with self.assertRaises(MatchNotFoundException):
            self.db_match_repository.end_match(0, None)
