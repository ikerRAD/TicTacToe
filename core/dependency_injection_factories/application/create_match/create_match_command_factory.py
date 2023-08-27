from core.application.create_match.create_match_command import CreateMatchCommand
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)


class CreateMatchCommandFactory:
    @staticmethod
    def create() -> CreateMatchCommand:
        return CreateMatchCommand(
            match_repository=DbMatchRepositoryFactory.create(),
        )
