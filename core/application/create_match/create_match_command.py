from core.application.command import Command
from core.application.create_match.create_match_command_info import (
    CreateMatchCommandInfo,
)
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class CreateMatchCommand(Command):
    __slots__ = "__match_repository"

    def __init__(self, match_repository: MatchRepository):
        self.__match_repository = match_repository

    def handle(self, creator: User) -> None:
        created_match = self.__match_repository.save(creator)

        raise CreateMatchCommandInfo(created_match.id)
