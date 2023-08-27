from core.application.join_match.join_match_command import JoinMatchCommand
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)


class JoinMatchCommandFactory:
    @staticmethod
    def create() -> JoinMatchCommand:
        return JoinMatchCommand(match_repository=DbMatchRepositoryFactory.create())
