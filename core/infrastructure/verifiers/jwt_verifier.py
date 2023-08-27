from typing import Any

from django.conf import settings

import jwt

from core.domain.exceptions.jwt_verification_exception import JWTVerificationException


class JWTVerifier:
    def verify(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            raise JWTVerificationException()
