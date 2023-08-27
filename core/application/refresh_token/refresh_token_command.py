from core.application.command import Command
from core.application.refresh_token.refresh_token_command_info import (
    RefreshTokenCommandInfo,
)
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.domain.repositories.user_repository import UserRepository
from core.infrastructure.verifiers.jwt_verifier import JWTVerifier


class RefreshTokenCommand(Command):
    __slots__ = ("__user_repository", "__jwt_verifier")

    def __init__(self, user_repository: UserRepository, jwt_verifier: JWTVerifier):
        self.__user_repository = user_repository
        self.__jwt_verifier = jwt_verifier

    def handle(self, refresh_token: str) -> None:
        payload = self.__jwt_verifier.verify(refresh_token)

        user_id = payload.get("user_id")

        user = self.__user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundException()

        raise RefreshTokenCommandInfo(user)
