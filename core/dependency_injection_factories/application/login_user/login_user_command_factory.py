from core.application.login_user.login_user_command import LoginUserCommand
from core.dependency_injection_factories.infrastructure.repositories.db_user_repository_factory import (
    DbUserRepositoryFactory,
)


class LoginUserCommandFactory:
    @staticmethod
    def create() -> LoginUserCommand:
        return LoginUserCommand(
            user_repository=DbUserRepositoryFactory.create(),
        )
