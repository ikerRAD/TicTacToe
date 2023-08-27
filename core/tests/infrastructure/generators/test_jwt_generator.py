from unittest import TestCase
from unittest.mock import Mock

from freezegun import freeze_time

from core.domain.models.user import User
from core.infrastructure.generators.jwt_generator import JWTGenerator


class TestJWTGenerator(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = Mock(spec=User, id=1)

    def setUp(self) -> None:
        self.jwt_generator = JWTGenerator()

    @freeze_time("2023-08-22")
    def test_generate_access(self) -> None:
        expected_jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiO"
            "jE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9."
            "r-2WjLeEj8_-6zf4wbYs9-oqr2FWd93YiUmn2itnSzw"
        )

        retrieved_jwt = self.jwt_generator.generate(self.user)

        self.assertEqual(expected_jwt, retrieved_jwt)

    @freeze_time("2023-08-22")
    def test_generate_refresh(self) -> None:
        expected_jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiO"
            "jE2OTI3NDg4MDAsImlhdCI6MTY5MjY2MjQwMCwicmVmcmVzaF90b2tlbiI6dHJ"
            "1ZX0.MQNTszhO0rDP13hXfXwiNE4qORHz7De4lTJFHBKL8s8"
        )

        retrieved_jwt = self.jwt_generator.generate(self.user, refresh_token=True)

        self.assertEqual(expected_jwt, retrieved_jwt)
