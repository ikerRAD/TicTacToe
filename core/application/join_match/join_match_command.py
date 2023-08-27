from core.application.command import Command
from core.domain.models.user import User
from core.domain.repositories.match_repository import MatchRepository


class JoinMatchCommand(Command):
    __slots__ = "__match_repository"

    def __init__(self, match_repository: MatchRepository):
        self.__match_repository = match_repository

    def handle(self, guest: User, match_id: int) -> None:
        self.__match_repository.save_guest(guest, match_id)
