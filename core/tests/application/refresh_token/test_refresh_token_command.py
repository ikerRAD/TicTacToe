from unittest import TestCase
from unittest.mock import Mock

from core.application.refresh_token.refresh_token_command import RefreshTokenCommand
from core.application.refresh_token.refresh_token_command_info import (
    RefreshTokenCommandInfo,
)
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository
from core.infrastructure.verifiers.jwt_verifier import JWTVerifier


class TestRefreshTokenCommand(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User(id=1, username="user1", password="abcd")

    def setUp(self) -> None:
        self.user_repository = Mock(spec=UserRepository)
        self.jwt_verifier = Mock(spec=JWTVerifier)
        self.command = RefreshTokenCommand(self.user_repository, self.jwt_verifier)

    def test_handle(self) -> None:
        self.jwt_verifier.verify.return_value = {"user_id": 1}
        self.user_repository.find_by_user_id.return_value = self.user

        with self.assertRaises(RefreshTokenCommandInfo) as e:
            self.command.handle("access_token")

            self.assertEqual(self.user, e.user)

        self.jwt_verifier.verify.assert_called_once_with("access_token")
        self.user_repository.find_by_user_id.assert_called_once_with(1)

    def test_handle_no_user(self) -> None:
        self.jwt_verifier.verify.return_value = {"user_id": 5}
        self.user_repository.find_by_user_id.return_value = None

        with self.assertRaises(UserNotFoundException):
            self.command.handle("access_token")

        self.jwt_verifier.verify.assert_called_once_with("access_token")
        self.user_repository.find_by_user_id.assert_called_once_with(5)
