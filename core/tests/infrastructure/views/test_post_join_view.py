from django.test import TestCase
from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.match import Match
from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestIntegrationPostJoinView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User(id=2, username="user", password="1234")
        cls.user.save()

        cls.guest = User(id=1, username="user2", password="1234")
        cls.guest.save()

        cls.auth_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2"
            "VyX2lkIjoxLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2M"
            "jQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.r-2WjLeEj8_-6zf4"
            "wbYs9-oqr2FWd93YiUmn2itnSzw"
        )

        cls.match = Match(id=1, first_player=cls.user)
        cls.match.save()

        cls.started_match = Match(id=2, first_player=cls.user, status="in progress")
        cls.started_match.save()

        cls.guest_match = Match(id=3, first_player=cls.guest)
        cls.guest_match.save()

    def test_post(self) -> None:
        url = reverse("join_match", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/1/join/", url)
        self.assertEqual(204, retrieved_response.status_code)

    def test_unauthorized_post(self) -> None:
        url = reverse("join_match", kwargs={"match_id": 1})

        retrieved_response = self.client.post(url)

        self.assertEqual("/matches/1/join/", url)
        self.assertEqual(401, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Authentication failed"}',
            retrieved_response.content,
        )

    def test_post_match_started(self) -> None:
        url = reverse("join_match", kwargs={"match_id": 2})

        retrieved_response = self.client.post(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/2/join/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Match already started"}',
            retrieved_response.content,
        )

    def test_post_repeated_player(self) -> None:
        url = reverse("join_match", kwargs={"match_id": 3})

        retrieved_response = self.client.post(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/3/join/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Player already in match"}',
            retrieved_response.content,
        )

    def test_post_match_not_found(self) -> None:
        url = reverse("join_match", kwargs={"match_id": 0})

        retrieved_response = self.client.post(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/0/join/", url)
        self.assertEqual(404, retrieved_response.status_code)
