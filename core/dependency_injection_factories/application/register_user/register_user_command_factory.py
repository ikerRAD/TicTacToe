from core.application.register_user.register_user_command import RegisterUserCommand
from core.dependency_injection_factories.infrastructure.repositories.db_user_repository_factory import (
    DbUserRepositoryFactory,
)


class RegisterUserCommandFactory:
    @staticmethod
    def create() -> RegisterUserCommand:
        return RegisterUserCommand(
            user_repository=DbUserRepositoryFactory.create(),
        )
