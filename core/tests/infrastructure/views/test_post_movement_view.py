from django.test import TestCase
from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.match import Match
from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestIntegrationPostJoinView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(id=1, username="user1", password="1234")
        cls.guest = User.objects.create(id=2, username="user2", password="1234")
        cls.guest2 = User.objects.create(id=3, username="user3", password="1234")

        cls.auth_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2"
            "VyX2lkIjoxLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2M"
            "jQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.r-2WjLeEj8_-6zf4"
            "wbYs9-oqr2FWd93YiUmn2itnSzw"
        )

        cls.guest_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX"
            "2lkIjozLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMC"
            "wicmVmcmVzaF90b2tlbiI6ZmFsc2V9.deYZBfghkuB5e3iOStB-kpq"
            "qIH26r2nFWDwnbZSfiuc"
        )

        cls.match = Match.objects.create(
            id=1, first_player=cls.user, second_player=cls.guest, status="in progress"
        )

        cls.finished_match = Match.objects.create(
            id=2, first_player=cls.user, second_player=cls.guest, status="finished"
        )

    def test_post(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url,
            data={"x": 0, "y": 0},
            headers={"Authorization": self.auth_token},
            content_type="application/json",
        )

        self.assertEqual("/matches/1/movements/", url)
        self.assertEqual(204, retrieved_response.status_code)

    def test_unauthorized_post(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url,
            {"x": 0, "y": 0},
            content_type="application/json",
        )

        self.assertEqual("/matches/1/movements/", url)
        self.assertEqual(401, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Authentication failed"}',
            retrieved_response.content,
        )

    def test_post_invalid_schema(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url,
            {"x": 0},
            headers={"Authorization": self.auth_token},
            content_type="application/json",
        )

        self.assertEqual("/matches/1/movements/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "required key not provided @ data[\'y\']"}',
            retrieved_response.content,
        )

    def test_post_cannot_receive(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 2})

        retrieved_response = self.client.post(
            url,
            {"x": 0, "y": 0},
            headers={"Authorization": self.auth_token},
            content_type="application/json",
        )

        self.assertEqual("/matches/2/movements/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Match cannot receive more movements"}',
            retrieved_response.content,
        )

    def test_post_illegal_movement(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url,
            {"x": 3, "y": 3},
            headers={"Authorization": self.auth_token},
            content_type="application/json",
        )

        self.assertEqual("/matches/1/movements/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "The movement cannot be performed"}',
            retrieved_response.content,
        )

    def test_post_external_user_movement(self) -> None:
        url = reverse("make_movement", kwargs={"match_id": 1})

        retrieved_response = self.client.post(
            url,
            {"x": 2, "y": 2},
            headers={"Authorization": self.guest_token},
            content_type="application/json",
        )

        self.assertEqual("/matches/1/movements/", url)
        self.assertEqual(403, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "The user with id 3 cannot perform a movement for the match with id 1"}',
            retrieved_response.content,
        )
