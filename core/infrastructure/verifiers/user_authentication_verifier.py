from typing import Optional

from django.http import HttpRequest

from core.domain.exceptions.jwt_verification_exception import JWTVerificationException
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository
from core.infrastructure.verifiers.jwt_verifier import JWTVerifier


class UserAuthenticationVerifier:
    __slots__ = ("__user_repository", "__jwt_verifier")

    def __init__(self, user_repository: UserRepository, jwt_verifier: JWTVerifier):
        self.__user_repository = user_repository
        self.__jwt_verifier = jwt_verifier

    def verify(self, request: HttpRequest) -> User:
        token = self.__extract_token(request)

        try:
            payload = self.__jwt_verifier.verify(token)
        except JWTVerificationException:
            raise UserAuthenticationException()

        user = self.__user_repository.find_by_id(payload.get("user_id"))

        if user is None:
            raise UserAuthenticationException()

        return user

    def __extract_token(self, request: HttpRequest) -> str:
        authorization_header: Optional[str] = request.META.get(
            "HTTP_AUTHORIZATION", None
        )

        if authorization_header is None:
            raise UserAuthenticationException()

        return authorization_header.split(" ")[1]
