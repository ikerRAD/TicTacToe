from core.application.get_match.get_match_query import GetMatchQuery
from core.dependency_injection_factories.infrastructure.generators.board_generator_factory import (
    BoardGeneratorFactory,
)
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)


class GetMatchQueryFactory:
    @staticmethod
    def create() -> GetMatchQuery:
        return GetMatchQuery(
            match_repository=DbMatchRepositoryFactory.create(),
            board_generator=BoardGeneratorFactory.create(),
        )
