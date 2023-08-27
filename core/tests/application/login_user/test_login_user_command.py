from unittest import TestCase
from unittest.mock import Mock

from core.application.login_user.login_user_command import LoginUserCommand
from core.application.login_user.login_user_command_info import LoginUserCommandInfo
from core.domain.exceptions.incorrect_user_password_exception import (
    IncorrectUserPasswordException,
)
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository


class TestLoginUserCommand(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User(id=1, username="user1", password="abcd")

    def setUp(self) -> None:
        self.user_repository = Mock(spec=UserRepository)
        self.command = LoginUserCommand(self.user_repository)

    def test_handle(self) -> None:
        self.user_repository.find_user_by_username.return_value = self.user

        with self.assertRaises(LoginUserCommandInfo) as e:
            self.command.handle("user1", "abcd")

            self.assertEqual(e.user, self.user)

        self.user_repository.find_user_by_username.assert_called_once_with("user1")

    def test_handle_no_user(self) -> None:
        self.user_repository.find_user_by_username.return_value = None

        with self.assertRaises(UserNotFoundException):
            self.command.handle("user3", "abcd")

        self.user_repository.find_user_by_username.assert_called_once_with("user3")

    def test_handle_fails_password(self) -> None:
        self.user_repository.find_user_by_username.return_value = self.user

        with self.assertRaises(IncorrectUserPasswordException):
            self.command.handle("user1", "abc2d")

        self.user_repository.find_user_by_username.assert_called_once_with("user1")
