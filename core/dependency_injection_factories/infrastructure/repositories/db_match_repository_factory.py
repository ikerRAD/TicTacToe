from core.infrastructure.repositories.db_match_repository import DbMatchRepository


class DbMatchRepositoryFactory:
    @staticmethod
    def create() -> DbMatchRepository:
        return DbMatchRepository()
