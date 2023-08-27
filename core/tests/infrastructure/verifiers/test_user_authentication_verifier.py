from unittest import TestCase
from unittest.mock import Mock

from django.http import HttpRequest

from core.domain.exceptions.jwt_verification_exception import JWTVerificationException
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository
from core.infrastructure.verifiers.jwt_verifier import JWTVerifier
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class TestUSerAuthenticationVerifier(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User(id=1, username="user", password="1234")

    def setUp(self) -> None:
        self.user_repository = Mock(spec=UserRepository)
        self.jwt_verifier = Mock(spec=JWTVerifier)
        self.user_auth_verifier = UserAuthenticationVerifier(
            self.user_repository, self.jwt_verifier
        )
        self.request = Mock(spec=HttpRequest)
        self.request.META = {"HTTP_AUTHORIZATION": "Bearer ey29..."}

    def test_verify(self) -> None:
        self.jwt_verifier.verify.return_value = {"user_id": 1}
        self.user_repository.find_by_user_id.return_value = self.user

        user = self.user_auth_verifier.verify(self.request)

        self.assertEqual(self.user, user)
        self.jwt_verifier.verify.assert_called_once_with("ey29...")
        self.user_repository.find_by_user_id.assert_called_once_with(1)

    def test_verify_no_token(self) -> None:
        self.request.META = {}

        with self.assertRaises(UserAuthenticationException):
            self.user_auth_verifier.verify(self.request)

        self.jwt_verifier.verify.assert_not_called()
        self.user_repository.find_by_user_id.assert_not_called()

    def test_verify_invalid_token(self) -> None:
        self.jwt_verifier.verify.side_effect = JWTVerificationException()

        with self.assertRaises(UserAuthenticationException):
            self.user_auth_verifier.verify(self.request)

        self.jwt_verifier.verify.assert_called_once_with("ey29...")
        self.user_repository.find_by_user_id.assert_not_called()

    def test_verify_no_user(self) -> None:
        self.jwt_verifier.verify.return_value = {"user_id": 2}
        self.user_repository.find_by_user_id.return_value = None

        with self.assertRaises(UserAuthenticationException):
            self.user_auth_verifier.verify(self.request)

        self.jwt_verifier.verify.assert_called_once_with("ey29...")
        self.user_repository.find_by_user_id.assert_called_once_with(2)
