from unittest import TestCase
from unittest.mock import Mock

from freezegun import freeze_time

from core.domain.exceptions.jwt_verification_exception import JWTVerificationException
from core.domain.models.user import User
from core.infrastructure.verifiers.jwt_verifier import JWTVerifier


class TestJWTVerifier(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = Mock(spec=User, id=1)

    def setUp(self) -> None:
        self.jwt_verifier = JWTVerifier()

    @freeze_time("2023-08-22")
    def test_verify(self) -> None:
        jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiO"
            "jE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9."
            "r-2WjLeEj8_-6zf4wbYs9-oqr2FWd93YiUmn2itnSzw"
        )

        payload = self.jwt_verifier.verify(jwt)

        self.assertEqual(
            {
                "user_id": 1,
                "exp": 1692748800,
                "iat": 1692662400,
                "refresh_token": False,
            },
            payload,
        )

    @freeze_time("2023-08-22")
    def test_verify_fails(self) -> None:
        jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiO"
            "jE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2tlbiI6dHJ"
            "1ZX0.MQNTszhO0rDP13hXfXwiNE4qORHz7DeFHBKL8s8"
        )

        with self.assertRaises(JWTVerificationException):
            self.jwt_verifier.verify(jwt)
