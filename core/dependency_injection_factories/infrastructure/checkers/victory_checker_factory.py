from core.dependency_injection_factories.infrastructure.generators.board_generator_factory import (
    BoardGeneratorFactory,
)
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)
from core.infrastructure.checkers.victory_checker import VictoryChecker


class VictoryCheckerFactory:
    @staticmethod
    def create() -> VictoryChecker:
        return VictoryChecker(
            match_repository=DbMatchRepositoryFactory.create(),
            board_generator=BoardGeneratorFactory.create(),
        )
