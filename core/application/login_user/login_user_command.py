from typing import Optional

from django.contrib.auth.hashers import check_password

from core.application.command import Command
from core.application.login_user.login_user_command_info import LoginUserCommandInfo
from core.domain.exceptions.incorrect_user_password_exception import (
    IncorrectUserPasswordException,
)
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository


class LoginUserCommand(Command):
    __slots__ = ("username", "password", "__user_repository")

    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def handle(self, username: str, password: str) -> None:
        user: Optional[User] = self.__user_repository.find_user_by_username(username)

        if user is None:
            raise UserNotFoundException()

        if check_password(password, user.password) is False:
            raise IncorrectUserPasswordException()

        raise LoginUserCommandInfo(user)
