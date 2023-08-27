from core.application.make_movement.make_movement_command import MakeMovementCommand
from core.dependency_injection_factories.infrastructure.checkers.victory_checker_factory import (
    VictoryCheckerFactory,
)
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)
from core.dependency_injection_factories.infrastructure.repositories.db_movement_repository_factory import (
    DbMovementRepositoryFactory,
)


class MakeMovementCommandFactory:
    @staticmethod
    def create() -> MakeMovementCommand:
        return MakeMovementCommand(
            movement_repository=DbMovementRepositoryFactory.create(),
            victory_checker=VictoryCheckerFactory.create(),
            match_repository=DbMatchRepositoryFactory.create(),
        )
