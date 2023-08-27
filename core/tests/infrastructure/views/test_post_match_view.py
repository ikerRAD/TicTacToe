from django.test import TestCase
from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestIntegrationPostMatchView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User(id=1, username="user", password="1234")
        user.save()

        cls.auth_token = (
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2"
            "VyX2lkIjoxLCJleHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2M"
            "jQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.r-2WjLeEj8_-6zf4"
            "wbYs9-oqr2FWd93YiUmn2itnSzw"
        )

    def test_post(self) -> None:
        url = reverse("create_match")

        retrieved_response = self.client.post(
            url, headers={"Authorization": self.auth_token}
        )

        self.assertEqual("/matches/", url)
        self.assertEqual(201, retrieved_response.status_code)

    def test_unauthorized_post(self) -> None:
        url = reverse("create_match")

        retrieved_response = self.client.post(url)

        self.assertEqual("/matches/", url)
        self.assertEqual(401, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Authentication failed"}',
            retrieved_response.content,
        )
