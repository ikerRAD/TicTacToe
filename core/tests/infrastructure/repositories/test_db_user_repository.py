from django.contrib.auth.hashers import check_password
from django.test import TestCase

from core.domain.models.user import User
from core.infrastructure.repositories.db_user_repository import DbUserRepository


class TestIntegrationDbUserRepository(TestCase):
    def setUp(self) -> None:
        self.db_user_repository = DbUserRepository()

    def test_save(self) -> None:
        users: list[User] = list(User.objects.all())
        self.assertEqual([], users)

        self.db_user_repository.save("user_test", "test")

        users: list[User] = list(User.objects.all())
        self.assertEqual(1, len(users))

        user = users[0]
        self.assertEqual("user_test", user.username)
        self.assertTrue(check_password("test", user.password))

        user.delete()