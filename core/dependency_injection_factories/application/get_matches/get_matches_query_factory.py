from core.application.get_matches.get_matches_query import GetMatchesQuery
from core.dependency_injection_factories.infrastructure.repositories.db_match_repository_factory import (
    DbMatchRepositoryFactory,
)


class GetMatchesQueryFactory:
    @staticmethod
    def create() -> GetMatchesQuery:
        return GetMatchesQuery(match_repository=DbMatchRepositoryFactory.create())
