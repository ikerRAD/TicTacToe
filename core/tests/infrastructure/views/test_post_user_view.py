from django.http import JsonResponse
from django.test import TestCase
from rest_framework.reverse import reverse

from core.domain.models.user import User


class TestIntegrationPostUserView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        existing_user = User(id=1, username="user", password="1234")
        existing_user.save()

    def test_post(self) -> None:
        url = reverse("create_user")

        retrieved_response = self.client.post(
            url,
            {"username": "user1", "password": "1234"},
            content_type="application/json",
        )

        self.assertEqual("/users/", url)
        self.assertEqual(201, retrieved_response.status_code)

    def test_post_invalid_schema(self) -> None:
        url = reverse("create_user")

        retrieved_response = self.client.post(
            url, {"password": "1234"}, content_type="application/json"
        )

        self.assertEqual("/users/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "required key not provided @ data[\'username\']"}',
            retrieved_response.content,
        )

    def test_post_user_already_exists(self) -> None:
        url = reverse("create_user")

        retrieved_response: JsonResponse = self.client.post(
            url,
            {"username": "user", "password": "1234"},
            content_type="application/json",
        )

        self.assertEqual("/users/", url)
        self.assertEqual(400, retrieved_response.status_code)
        self.assertEqual(
            b'{"error": "User already exists"}',
            retrieved_response.content,
        )
