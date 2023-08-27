from django.db.utils import IntegrityError

from core.application.command import Command
from core.application.register_user.register_user_command_info import RegisterUserCommandInfo
from core.domain.exceptions.user_already_exists_exception import UserAlreadyExistsException
from core.domain.repositories.user_repository import UserRepository


class RegisterUserCommand(Command):
    __slots__ = ('username', 'password', '__user_repository')

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, username: str, password: str) -> None:
        try:
            user = self.__user_repository.save(username, password)
        except IntegrityError:
            raise UserAlreadyExistsException(username)

        raise RegisterUserCommandInfo(user)
