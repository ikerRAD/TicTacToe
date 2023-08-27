from django.test import TestCase

from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.match import Match
from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestGetMatchesView(TestCase):
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

        cls.awaiting_match = Match.objects.create(id=1, first_player=cls.user)

    def test_get(self) -> None:
        url = reverse("get_matches")

        retrieved_response = self.client.get(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/all/", url)
        self.assertEqual(200, retrieved_response.status_code)
        self.assertEqual(
            b'{"count":1,"next":null,"previous":null,'
            b'"results":[{"id":1,"status":"awaiting","number_of_movements":0}]}',
            retrieved_response.content,
        )

    def test_unauthorized_get(self) -> None:
        url = reverse("get_matches")

        retrieved_response = self.client.get(url)

        self.assertEqual("/matches/all/", url)
        self.assertEqual(401, retrieved_response.status_code)
        self.assertEqual(
            b'{"error":"Authentication failed"}',
            retrieved_response.content,
        )
