from django.http import JsonResponse
from django.test import TestCase
from freezegun import freeze_time
from rest_framework.reverse import reverse

from core.domain.models.user import User


@freeze_time("2023-08-22")
class TestIntegrationPostRefreshView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        existing_user = User(id=1, username="user", password="1234")
        existing_user.save()

        cls.refresh_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJl"
            "eHAiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2"
            "tlbiI6dHJ1ZX0.MQNTszhO0rDP13hXfXwiNE4qORHz7De4lTJFHBKL8s8"
        )
        cls.invalid_user_refresh_token = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleH"
            "AiOjE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2tlbi"
            "I6dHJ1ZX0.QV_8wwo7xo6XUBvOrj5hxAIi3cW07klGhEYfJflX_aA"
        )

    def test_post(self) -> None:
        url = reverse("refresh_token")

        retrieved_response = self.client.post(
            url,
            {"refresh_token": self.refresh_token},
            content_type="application/json",
        )

        self.assertEqual("/login/refresh/", url)
        self.assertEqual(200, retrieved_response.status_code)

    def test_post_invalid_schema(self) -> None:
        url = reverse("refresh_token")

        retrieved_response = self.client.post(url, {}, content_type="application/json")

        self.assertEqual("/login/refresh/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "required key not provided @ data[\'refresh_token\']"}',
            retrieved_response.content,
        )

    def test_post_incorrect_user(self) -> None:
        url = reverse("refresh_token")

        retrieved_response: JsonResponse = self.client.post(
            url,
            {"refresh_token": self.invalid_user_refresh_token},
            content_type="application/json",
        )

        self.assertEqual("/login/refresh/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "Invalid refresh token"}',
            retrieved_response.content,
        )
