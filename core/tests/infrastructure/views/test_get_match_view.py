from django.test import TestCase
from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.match import Match
from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestGetMatchView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(id=1, username="user", password="1234")

        cls.guest = User.objects.create(id=2, username="user2", password="1234")

        cls.auth_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2"
            "VyX2lkIjoxLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2M"
            "jQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.r-2WjLeEj8_-6zf4"
            "wbYs9-oqr2FWd93YiUmn2itnSzw"
        )
        cls.guest_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo"
            "yLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVm"
            "cmVzaF90b2tlbiI6ZmFsc2V9.kasudsrg6mHNLoCNkGySlKgQbHErO"
            "DxxhtZZMHdxXks"
        )

        cls.awaiting_match = Match.objects.create(first_player=cls.user)
        cls.match = Match.objects.create(
            first_player=cls.user, second_player=cls.guest, status="in progress"
        )
        cls.finished_match = Match.objects.create(
            first_player=cls.user,
            second_player=cls.guest,
            status="finished",
            winner=cls.user,
        )

    def test_get(self) -> None:
        url = reverse("get_match", kwargs={"match_id": self.match.id})

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual(f"/matches/{self.match.id}/", url)
        self.assertEqual(200, retrieved_response.status_code)
        self.assertEqual(
            b'{"status": "in progress", "number_of_movements": 0, '
            b'"board": [[null, null, null], [null, null, null], [null, null, null]], '
            b'"first_player_id": 1, "first_player_username": "user", '
            b'"second_player_id": 2, "second_player_username": "user2"}',
            retrieved_response.content,
        )

    def test_get_winner(self) -> None:
        url = reverse("get_match", kwargs={"match_id": self.finished_match.id})

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual(f"/matches/{self.finished_match.id}/", url)
        self.assertEqual(200, retrieved_response.status_code)
        self.assertEqual(
            b'{"status": "finished", "number_of_movements": 0, '
            b'"board": [[null, null, null], [null, null, null], [null, null, null]], '
            b'"first_player_id": 1, "first_player_username": "user", '
            b'"second_player_id": 2, "second_player_username": "user2", '
            b'"winner": "first player"}',
            retrieved_response.content,
        )

    def test_get_awaiting(self) -> None:
        url = reverse("get_match", kwargs={"match_id": self.awaiting_match.id})

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual(f"/matches/{self.awaiting_match.id}/", url)
        self.assertEqual(200, retrieved_response.status_code)
        self.assertEqual(
            b'{"status": "awaiting", "number_of_movements": 0, '
            b'"board": [[null, null, null], [null, null, null], [null, null, null]], '
            b'"first_player_id": 1, "first_player_username": "user"}',
            retrieved_response.content,
        )

    def test_unauthorized_get(self) -> None:
        url = reverse("get_match", kwargs={"match_id": self.match.id})

        retrieved_response = self.client.get(url)

        self.assertEqual(f"/matches/{self.match.id}/", url)
        self.assertEqual(401, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Authentication failed"}',
            retrieved_response.content,
        )

    def test_get_non_existing_match(self) -> None:
        url = reverse("get_match", kwargs={"match_id": 0})

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/0/", url)
        self.assertEqual(404, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Match not found"}',
            retrieved_response.content,
        )

    def test_get_not_in_game(self) -> None:
        url = reverse("get_match", kwargs={"match_id": self.awaiting_match.id})

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.guest_token}
        )

        self.assertEqual(f"/matches/{self.awaiting_match.id}/", url)
        self.assertEqual(403, retrieved_response.status_code)
