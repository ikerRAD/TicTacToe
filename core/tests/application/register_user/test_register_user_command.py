from unittest import TestCase
from unittest.mock import Mock

from django.db import IntegrityError

from core.application.register_user.register_user_command import RegisterUserCommand
from core.application.register_user.register_user_command_info import (
    RegisterUserCommandInfo,
)
from core.domain.exceptions.user_already_exists_exception import (
    UserAlreadyExistsException,
)
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository


class TestRegisterUserCommand(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = Mock(spec=User, id=1, username="user1", password="abcd")

    def setUp(self) -> None:
        self.user_repository = Mock(spec=UserRepository)
        self.command = RegisterUserCommand(self.user_repository)

    def test_handle(self) -> None:
        self.user_repository.save.return_value = self.user

        with self.assertRaises(RegisterUserCommandInfo) as e:
            self.command.handle("user1", "abcd")

            self.assertEqual(e.user, self.user)

        self.user_repository.save.assert_called_once_with("user1", "abcd")

    def test_handle_fails(self) -> None:
        self.user_repository.save.side_effect = IntegrityError()

        with self.assertRaises(UserAlreadyExistsException):
            self.command.handle("user1", "abcd")

        self.user_repository.save.assert_called_once_with("user1", "abcd")
