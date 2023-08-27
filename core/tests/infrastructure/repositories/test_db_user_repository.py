from django.contrib.auth.hashers import check_password
from django.test import TestCase

from core.domain.models.user import User
from core.infrastructure.repositories.db_user_repository import DbUserRepository


class TestIntegrationDbUserRepository(TestCase):
    def setUp(self) -> None:
        self.db_user_repository = DbUserRepository()

    def test_find_user_by_id(self) -> None:
        existing_user = User(id=1, username="user", password="123")
        existing_user.save()

        user = self.db_user_repository.find_by_id(1)

        self.assertEquals(existing_user, user)

        existing_user.delete()

    def test_find_user_by_id_fails(self) -> None:
        user = self.db_user_repository.find_by_id(0)

        self.assertIsNone(user)

    def test_find_user_by_username(self) -> None:
        existing_user = User(username="user", password="123")
        existing_user.save()

        user = self.db_user_repository.find_user_by_username("user")

        self.assertEquals(existing_user, user)

        existing_user.delete()

    def test_find_user_by_username_fails(self) -> None:
        user = self.db_user_repository.find_user_by_username("usr")

        self.assertIsNone(user)

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
